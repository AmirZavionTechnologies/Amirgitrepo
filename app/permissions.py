from rest_framework.permissions import BasePermission

class CanViewResidentsData(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is an admin
        return request.user.is_superuser

class IsAdminOrResidentUser(BasePermission):
    """
    Allows access only to admin or resident users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'resident')
