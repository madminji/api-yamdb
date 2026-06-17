from rest_framework import serializers


USERNAME_REGEX = r'^[\w.@+-]+\Z'

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        max_length=150,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                "Использование имени 'me' запрещено."
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
        max_length=150,
    )
    confirmation_code = serializers.CharField(write_only=True)
