import re

from django.conf import settings
from rest_framework import serializers

from reviews.models import Category, Genre, Title, User

USERNAME_REGEX = re.compile(r'^[\w.@+-]+\Z', re.ASCII)


def validate_not_me(value):
    if value.lower() == 'me':
        raise serializers.ValidationError(
            "Использование имени 'me' запрещено."
        )
    return value


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=settings.EMAIL_MAX_LENGTH)
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        max_length=settings.USERNAME_MAX_LENGTH,
    )

    def validate_username(self, value):
        return validate_not_me(value)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()
        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError(
                {'username': 'Username уже занят!'}
            )
        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError(
                {'email': 'Email уже занят!'}
            )
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
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        return validate_not_me(value)


class MeSerializer(UserSerializer):
    role = serializers.CharField(read_only=True)


class CatGenSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta(CatGenSerializer.Meta):
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta(CatGenSerializer.Meta):
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Title
