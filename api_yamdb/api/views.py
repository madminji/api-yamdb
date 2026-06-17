from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, Token

from reviews.models import User
from .serializers import SignUpSerializer, TokenSerializer


class ConfirmationToken(Token):
    token_type = 'confirmation'
    lifetime = timedelta(days=1)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=serializer.validated_data['username'],
        defaults={'email': serializer.validated_data['email']}
    )
    confirmation_code = str(ConfirmationToken.for_user(user))
    send_mail(
        subject='Код подтверждения YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


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
            {'confirmation_code': 'Неверный или просроченный код.'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    access_token = AccessToken.for_user(user)
    return Response({'token': str(access_token)}, status=status.HTTP_200_OK)
