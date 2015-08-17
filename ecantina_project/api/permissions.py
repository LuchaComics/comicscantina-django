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

class IsEmployeeUserOrReadOnly(permissions.BasePermission):
    """
        Custom permission to deny all non-employees from performing writing
        actions and allow all read-only actions instead. Employees are able
        to perform write actions.
    """
    message = 'Only employees are allowed to access data.'
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            # Check permissions for read-only request
            if request.method in permissions.SAFE_METHODS:
                # Note: Non-authenticated users are allowed to perform
                #       'read-only' actions on the data.
                return True
            else: # Check permissions for write request
                return False
        
        # Find employee object for the user
        try:
            Employee.objects.get(user=request.user)
            return True
        except Employee.DoesNotExist:
            return False


class IsOnlyOwnedByEmployee(permissions.BasePermission):
    """
        Object-level permission to only allow employees who own the object
        are thus given permission to access the employee.
    """
    message = 'Only employees who belong to the same organization are able to access data.'
    def has_object_permission(self, request, view, obj):
        employee = Employee.objects.get(user=request.user)
        
        # Instance must have an attribute named `organization`.
        return obj.employee == employee


class BelongsToOrganization(permissions.BasePermission):
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


class BelongsToOrganizationOrReadOnly(permissions.BasePermission):
    """
        Object-level permission to only allow employees who belong to the
        organization (of the object) be able to access/modify the object.
        If an employee from a different organization tries to access the object
        then permission will only be granted for read-only actions.
    """
    message = 'Only employees who belong to the same organization are able to write data.'
    def has_object_permission(self, request, view, obj):
        # Check permissions for read-only request
        if request.method in permissions.SAFE_METHODS:
            return True # Anyone can ead object.
        else: # Check permissions for write request
            # Do not allow write for users who have not logged on.
            if request.user.is_anonymous():
                return False

        try:
            employee = Employee.objects.get(user=request.user)
        
            # Instance must have an attribute named `organization`.
            return obj.organization == employee.organization
        except Employee.DoesNotExist:
            return False