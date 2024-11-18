from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'STUDENT'

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'TEACHER'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'

