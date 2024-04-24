import time
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, UserCreateSerializer
from .models import User
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view,\
    OpenApiParameter, OpenApiExample, OpenApiResponse
from drf_spectacular.types import OpenApiTypes


def send_code(phone_number, sent_code=None):
    time.sleep(2)


def confirm_code(received_code, sent_code=None):
    return True


@extend_schema(
responses={
status.HTTP_201_CREATED: OpenApiResponse(
    response=str,
    description='Номер телефона'),
status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=None,
            description='Ввод неверных данных'),
status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
    response=None,
    description='Ошибка сервера')})
@api_view(['POST', ])
@permission_classes((AllowAny, ))
def get_phone_view(request):
    """ Запрос номера телефона и кода подтверждения """
    phone_number = request.data.get('phone_number')
    if not phone_number:
        return Response(
            {'phone_number': 'Введите номер телефона'},
            status=status.HTTP_400_BAD_REQUEST)
    send_code(phone_number)
    received_code = request.data.get('received_code')
    if confirm_code(received_code):
        return Response({'phone_number': phone_number},
                        status=status.HTTP_200_OK)
    return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
request=UserCreateSerializer,
responses={
status.HTTP_201_CREATED: OpenApiResponse(
    response=str,
    description='Токен'),
status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=None,
            description='Ввод неверных данных'),
status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
    response=None,
    description='Ошибка сервера')})
@api_view(['POST', ])
@permission_classes((AllowAny, ))
def create_user(request):
    """ Создание пользователя и присвоение ему access-токена"""
    serializer = UserCreateSerializer(data=request.data)
    phone_number = request.data.get('phone_number')
    if User.objects.filter(phone_number=phone_number):
        user = User.objects.get(phone_number=request.data['phone_number'])
        token = RefreshToken.for_user(user)
        return Response(
            {str(token.access_token)},
            status=status.HTTP_201_CREATED
        )

    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(phone_number=phone_number)
    token = RefreshToken.for_user(user)
    return Response({'token': str(token.access_token)}, status=status.HTTP_201_CREATED)


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(
    request=UserSerializer,
    responses={
    status.HTTP_200_OK: UserSerializer,
    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=None,
        description='Ошибка авторизации'),
    status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
        response=None,
        description='Ошибка сервера')},
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=None,
            description='Пользователь вводит свой реферальный код'),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=None,
            description='Ошибка авторизации'),
        status.HTTP_403_FORBIDDEN: OpenApiResponse(
            response=None,
            description='Код уже введен'),
        status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
            response=None,
            description='Ошибка сервера')},
    )
    def patch(self, request):
        user = request.user
        if user.invite_code:
            return Response(
                {'invite_code': 'Код уже введен'},
                status=status.HTTP_403_FORBIDDEN)
        invite_code = request.data.get('invite_code', None)
        serializer = UserSerializer(user, data=request.data,
                                    partial=True)
        serializer.is_valid(raise_exception=True)
        if invite_code == user.referral_code:
            return Response(
                {'inviter_code': 'Это ваш код"'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return self.get(request)
