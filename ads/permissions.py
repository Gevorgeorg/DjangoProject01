from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user:
            return False

        return (obj.author == request.user or
                request.user.role in ['admin', 'moderator'] or
                request.user.is_staff)
