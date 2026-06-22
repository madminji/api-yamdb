from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User
from .validators import USERNAME_REGEX, validate_username_not_me


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
        fields = ('name', 'slug')


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

    def validate_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.'
            )
        return value

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'genre', 'category')
