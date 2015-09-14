from django.contrib.auth.models import User, AnonymousUser
from rest_framework import permissions
from api.models.ec.employee import Employee


class IsAdminUserOrReadOnly(permissions.BasePermission):
    message = 'Only administrators are allowed to write data.'
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else: # Check permissions for write request
            if request.user.is_anonymous():
                return False
            else:
                return request.user.is_superuser


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
        actions and allow all read-only actions instead. 
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


class BelongsToEmployee(permissions.BasePermission):
    """
        Object-level permission to only allow employees who own the object
        are thus given permission to access the employee.
    """
    message = 'Only employees who belong to the same organization are able to access data.'
    def has_object_permission(self, request, view, obj):
        try:
            employee = Employee.objects.get(user=request.user)
        
            # Instance must have an attribute named `organization`.
            return obj.employee == employee
        except Employee.DoesNotExist:
            return False

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


class BelongsToOrganizationOwnerOrReadOnly(permissions.BasePermission):
    """
        Object-level permission to only allow owners of the organization
        to be able to write to it, else it's readable to everyone else.
    """
    message = 'Only employees who are owners of the organization are able to write data.'
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
            return obj.org_id == employee.organization_id and obj.administrator == employee.user
        except Employee.DoesNotExist:
            return False


class BelongsToOrganizationOrCustomer(permissions.BasePermission):
    """
        Object-level permission to only allow employees who belong to the
        organization (of the object) be able to access/modify the object OR
        customers of the object. If an employee from a different organization 
        or different custoemr tries to access the object then permission denied 
        will occure.
    """
    message = 'Only employees who belong to the same organization, or the customer of the object are able to access data.'
    def has_object_permission(self, request, view, obj):
        try:
            employee = Employee.objects.get(user=request.user)
            return obj.organization == employee.organization
        except Employee.DoesNotExist:
            pass

        try:
            customer = Customer.object.get(user=request.user)
            return obj.customer == customer
        except Customer.DoesNotExist:
            return False


class BelongsToCustomerOrIsEmployeeUser(permissions.BasePermission):
    """
        Object-level permission to only allow customers who own the object
        be able to access/modify the object OR the logged in user is an
        employee.
    """
    message = 'Only employees or customer who own this object are able to access the data.'
    def has_object_permission(self, request, view, obj):
        try:
            Employee.objects.get(user=request.user)
            return True
        except Employee.DoesNotExist:
            pass

        try:
            customer = Customer.object.get(user=request.user)
            return obj.customer == customer
        except Customer.DoesNotExist:
            return False


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

