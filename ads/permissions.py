from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        """Разрешение для владельца, админа или модератора"""

        if request.method in permissions.SAFE_METHODS:
            return True


        return bool(obj.author == request.user or
           request.user.role in ['admin', 'moderator'])


class IsAdminOrModerator(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        """Разрешение только для админов"""

        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ['admin', 'moderator']
        )

    def has_object_permission(self, request, view, obj) -> bool:
        return self.has_permission(request, view)

