from rest_framework.permissions import BasePermission


class SuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser)


class SuperUserORAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser or request.user.is_company_admin)
