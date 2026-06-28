from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User, Review, Comment
from .validators import USERNAME_REGEX, validate_username_not_me

# Константы для оценки
MIN_SCORE = 1
MAX_SCORE = 10


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        max_length=settings.USERNAME_MAX_LENGTH,
        validators=(validate_username_not_me,),
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        errors = {}

        if user_by_username and user_by_username.email != email:
            errors['username'] = 'Username уже занят!'

        if user_by_email and user_by_email.username != username:
            errors['email'] = 'Email уже занят!'

        if errors:
            raise serializers.ValidationError(errors)

        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        max_length=settings.USERNAME_MAX_LENGTH,
    )
    confirmation_code = serializers.CharField(write_only=True)

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user,
                data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный или просроченный код.'},
            )
        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        return validate_username_not_me(value)


class MeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CatGenSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta(CatGenSerializer.Meta):
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta(CatGenSerializer.Meta):
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'genre', 'category',
                  'rating')


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_empty=False
    )

    def to_representation(self, instance):
        instance = (
            Title.objects
            .filter(pk=instance.pk)
            .annotate(rating=Avg('reviews__score'))
            .first()
        )
        return TitleReadSerializer(instance, context=self.context).data

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date')

    def validate_score(self, value):
        if not (MIN_SCORE <= value <= MAX_SCORE):
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_SCORE} до {MAX_SCORE}.'
            )
        return value

    def validate(self, data):
        request = self.context.get('request')
        if request and request.method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            if Review.objects.filter(
                    author=request.user,
                    title_id=title_id
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на это произведение.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date')
