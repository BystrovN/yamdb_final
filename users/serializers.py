from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер модели пользователя. Для администраторов."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Сериалайзер модели пользователя. Для пользователей."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class UserCreateSerializer(serializers.Serializer):
    """Сериалайзер для самостоятельной регистрации пользователей."""

    username = serializers.CharField(
        max_length=150, required=True, write_only=True
    )
    email = serializers.EmailField(required=True, write_only=True)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return value


class CreateJWTSerializer(serializers.Serializer):
    """Сериалайзер для получения пользователем JWT-токена."""

    username = serializers.CharField(
        max_length=150, required=True, write_only=True
    )
    confirmation_code = serializers.CharField(
        max_length=40, required=True, write_only=True
    )
