from rest_framework.permissions import BasePermission


class IsSchool(BasePermission):
    '''
    Allows access only to user who is School .
    '''

    def has_permission(self, request, view):
        return request.user.is_school


class IsStudent(BasePermission):
    '''
    Allows access only to user who is Student .
    '''

    def has_permission(self, request, view):
        return request.user.is_student


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsSchoolOrStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_school or request.user.is_student
