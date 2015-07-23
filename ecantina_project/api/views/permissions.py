from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions
from api.models.ec.employee import Employee

class IsEmployee(permissions.BasePermission):
    """
        Custom permission to deny all non-employees that are logged in.
    """
    def has_permission(self, request, view):
        # Reject Anonymous users.
        if request.user.is_anonymous():
            return False
        
        # Find employee object for the user
        try:
            Employee.objects.get(user=request.user)
            return True
        except Employee.DoesNotExist:
            return False