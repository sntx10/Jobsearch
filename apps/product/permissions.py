from rest_framework import permissions

from apps.catalog.models import Recruiter


class ReadOnlyOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow read-only access to all users, and full access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Позволяет редактировать и удалять объекты только их владельцам
    """
    def has_object_permission(self, request, view, obj):
        # Разрешить GET, HEAD, OPTIONS запросы для любых пользователей
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешить PUT, PATCH, DELETE запросы только владельцам объекта
        return obj.user == request.user


class CanCreateCompany(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated and user.can_create_company:
            return True
        return False


class IsRecruiterWithPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        recruiter = request.user.recruiter_users.first()
        if recruiter and recruiter.can_create_vacancy:
            return True
        return False
