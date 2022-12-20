from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from . import serializers
from .authentication import generate_confirmation_code
from .permissions import IsAdmin

User = get_user_model()


class UserView(ListCreateAPIView):
    """
    Представление для просмотра и создания записи в модели пользователей.
    """

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination


class UserDetailView(APIView):
    """
    Представление для редактирования и удаления записи из модели пользователей.
    """

    permission_classes = (IsAdmin,)
    serializer_class = serializers.UserSerializer

    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, username):
        user = get_object_or_404(User, username=username)
        serializer = self.serializer_class(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return Response(
            {'message': f'Пользователь {username} удален'},
            status=status.HTTP_204_NO_CONTENT,
        )


class UserMeView(APIView):
    """
    Представление для просмотра и редактирования
    пользователем информации о себе.
    """

    serializer_class_read = serializers.UserSerializer
    serializer_class_write = serializers.UserMeSerializer

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class_read(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.serializer_class_write(
            user, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NewUserView(APIView):
    """
    Представление для получения пользователем кода подтверждения на email.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            user, _ = User.objects.get_or_create(
                username=username, email=email
            )
            user.clean_fields(exclude=('confirmation_code', 'password'))
            confirmation_code = generate_confirmation_code()
            user.confirmation_code = confirmation_code
            user.save()

            send_mail(
                'YaMDb registration. Confirmation code',
                f'Your confirmation code - {confirmation_code}.',
                'from@example.com',
                (email,),
                fail_silently=False,
            )
            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JWTUserView(APIView):
    """
    Представление для получения пользователем JWT-токена.
    """

    permission_classes = (AllowAny,)
    serializer_class = serializers.CreateJWTSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            conf_code = serializer.validated_data.get('confirmation_code')
            user = get_object_or_404(
                User, username=serializer.validated_data.get('username')
            )

            if conf_code == user.confirmation_code:
                jwt_token = AccessToken.for_user(user)
                return Response(
                    {'access': f'{jwt_token}'},
                    status=status.HTTP_200_OK,
                )
            raise ValidationError('Неверный код подтверждения')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
