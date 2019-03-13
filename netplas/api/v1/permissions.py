from rest_framework.permissions import BasePermission


class DocumentAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_staff
