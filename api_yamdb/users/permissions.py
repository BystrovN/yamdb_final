from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """
    Предоставляем доступ только авторизованному
    пользователю с ролью администратора
    """

    def has_permission(self, request, view):
        if request.user.is_anonymous:
            raise NotAuthenticated('Необходим JWT-токен')

        if request.user.is_admin or request.user.is_superuser:
            return True

        raise PermissionDenied('Нет прав доступа')


class AdminOrReadOnly(BasePermission):
    """
    Просмотр доступен неавторизованному пользователю, добавление/редактирование
    объекта только авторизованному пользователю с ролью администратора.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_anonymous:
            raise NotAuthenticated('Необходим JWT-токен')

        if request.user.is_admin or request.user.is_superuser:
            return True

        raise PermissionDenied('Нет прав доступа')


class AuthorOrAdminOrReadOnly(BasePermission):
    """
    Просмотр доступен неавторизованному пользователю,
    добавление/редактирование объекта только автору
    или авторизованному пользователю с ролью администратора.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS or request.user.is_authenticated:
            return True

        if request.user.is_anonymous:
            raise NotAuthenticated('Необходим JWT-токен')

        raise PermissionDenied('Нет прав доступа')

    def has_object_permission(self, request, view, obj):
        if (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
            or request.user.is_superuser
        ):
            return True

        raise PermissionDenied('Нет прав доступа')
