from rest_framework.permissions import BasePermission

class IsValidUser(BasePermission):
    """
    Allows access only to users who have a valid JWT token.
    """
    def has_permission(self, request, view):
        # If CustomJWTAuthentication successfully found a user, this will be True
        return bool(request.user)