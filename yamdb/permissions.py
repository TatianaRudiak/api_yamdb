from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

from yamdb.models import UserRole

User = get_user_model()

MODERATOR_METHODS = ('PATCH', 'DELETE')


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.is_admin
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and request.user.role == UserRole.ADMIN
                or request.user.is_superuser)


class IsAuthorOrModerator(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in MODERATOR_METHODS
                and request.user.is_moderator
                or obj.author == request.user)
