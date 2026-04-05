
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Only Admin role users are allowed."""
    message = 'Access denied. Admin role required.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.is_admin
        )


class IsAnalystOrAdmin(BasePermission):
    """Analyst and Admin roles are allowed."""
    message = 'Access denied. Analyst or Admin role required.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
            and request.user.can_read_insights
        )


class IsAnyRole(BasePermission):
    """Any authenticated and active user is allowed (viewer, analyst, admin)."""
    message = 'Access denied. Active account required.'

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_active
        )


class IsAdminOrReadOnly(BasePermission):
    """
    Read access for all authenticated users.
    Write access only for Admin.
    """
    message = 'Access denied. Admin role required to modify records.'

    SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and request.user.is_active):
            return False
        if request.method in self.SAFE_METHODS:
            return True
        return request.user.is_admin
