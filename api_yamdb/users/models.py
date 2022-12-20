from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator

from .validators import validate_username


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        username = self.model.normalize_username(username)
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', CustomUser.ADMIN)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER = 'user'
    MODER = 'moderator'
    ADMIN = 'admin'
    ROLES = [(USER, 'user'), (MODER, 'moderator'), (ADMIN, 'admin')]

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(UnicodeUsernameValidator(), validate_username),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=9, choices=ROLES, default=USER)
    confirmation_code = models.CharField(
        max_length=40, unique=True, null=True
    )  # Длина == 40, так как secrets.token_hex(20) вернет объект с len == 40.

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    @property
    def is_moderator(self):
        return self.role == self.MODER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_staff(self):
        return self.is_admin
