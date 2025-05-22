from rest_framework.permissions import BasePermission

class IsChefOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name__in=['Admin', 'Chef']).exists()
            )
        )

class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                request.user.is_superuser or
                request.user.groups.filter(name__in=['Admin', 'Manager']).exists()
            )
        ) 