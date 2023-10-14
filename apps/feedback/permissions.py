from rest_framework.permissions import BasePermission
from django.contrib.auth import get_user_model

User = get_user_model()


class IsFavoriteOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATH']:
            return request.user.is_authenticated and request.user == obj.owner
        return request.user.is_authenticated and request.user == obj.owner