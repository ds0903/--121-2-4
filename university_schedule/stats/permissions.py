# university_schedule/stats/permissions.py
from rest_framework.permissions import BasePermission

class IsManagement(BasePermission):
    """
    Доступ має тільки автентифікований користувач з role='manager'
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(
            user and
            user.is_authenticated and
            user.role in ['manager','editor'] or user.is_superuser
        )

class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)