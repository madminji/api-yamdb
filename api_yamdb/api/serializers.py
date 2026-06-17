from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework import serializers

from reviews.models import User



class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[ASCIIUsernameValidator()]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использование имени 'me' запрещено."
            )
        return value

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()
        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError('Username уже занят!')
        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError('Email уже занят!')
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[ASCIIUsernameValidator()]
    )
    confirmation_code = serializers.CharField(write_only=True)