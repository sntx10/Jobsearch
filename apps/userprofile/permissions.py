from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsProfileOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (request.user == obj.user)