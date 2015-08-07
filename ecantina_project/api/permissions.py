from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions
from api.models.ec.employee import Employee

class IsEmployeeUser(permissions.BasePermission):
    """
        Custom permission to deny all non-employees that are logged in.
    """
    message = 'Only employees are allowed to access data.'
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

class IsEmployeeMemberOfOrganization(permissions.BasePermission):
    """
        Object-level permission to only allow employees who belong to the
        organization (of the object) be able to access/modify the object.
        If an employee from a different organization tries to access the object
        then permission denied will occure.
    """
    message = 'Only employees who belong to the same organization are able to access data.'
    def has_object_permission(self, request, view, obj):
        employee = Employee.objects.get(user=request.user)
        
        # Instance must have an attribute named `organization`.
        return obj.organization == employee.organization