from rest_framework import permissions

class IsEditor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'editor'

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'manager'

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'