from datetime import timedelta

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, Token

from reviews.models import User
from .serializers import SignUpSerializer, TokenSerializer


class ConfirmationToken(Token):
    """Кастомный JWT-токен для confirmation_code."""
    token_type = 'confirmation'
    lifetime = timedelta(days=1)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']

    user_by_email = User.objects.filter(email=email).first()
    user_by_name = User.objects.filter(username=username).first()

    if user_by_email and user_by_name != user_by_email:
        return Response(
            {'email': 'Этот email уже занят другим пользователем.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if user_by_name and user_by_name.email != email:
        return Response(
            {'username': 'Этот username уже занят другим пользователем.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user, _ = User.objects.get_or_create(
        username=username,
        defaults={'email': email},
    )

    confirmation_code = str(ConfirmationToken.for_user(user))

    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email='yamdb@yamdb.fake',
        recipient_list=[user.email],
    )

    return Response(
        {'username': username, 'email': email},
        status=status.HTTP_200_OK,
    )

@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    user = get_object_or_404(User, username=username)

    try:
        token = ConfirmationToken(confirmation_code)
        if token['user_id'] != user.pk:
            raise TokenError('user_id не совпадает')
    except TokenError:
        return Response(
            {'confirmation_code': 'Неверный или просроченный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    access_token = AccessToken.for_user(user)
    return Response({'token': str(access_token)}, status=status.HTTP_200_OK)
