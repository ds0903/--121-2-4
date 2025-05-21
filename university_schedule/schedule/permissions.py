from rest_framework import permissions

class IsAdminOrEditor(permissions.BasePermission):
    """
    Дозволяє доступ лише суперкористувачу (admin) або користувачу з role='editor'.
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and user.is_authenticated
            and (user.is_superuser or user.role == 'editor')
        )
