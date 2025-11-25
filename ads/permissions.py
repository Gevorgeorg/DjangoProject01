from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (obj.author == request.user or
                getattr(request.user, 'role', None) in ['admin', 'moderator'] or
                request.user.is_staff)
