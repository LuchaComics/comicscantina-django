from django.conf import settings
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser
from api.serializers import EmployeeSerializer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee

class EmployeeViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username', '=email')

    def list(self, request):
        employee = Employee.objects.get(user=self.request.user)
        employees = Employee.objects.filter(organization=employee.organization)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
            Note: A employee cannot delete an owner unless the user is staff.
        """
        employee = Employee.objects.get(user=self.request.user)
        
        # Workers cannot fire employees.
        if employee.role is settings.EMPLOYEE_WORKER_ROLE:
            return Response({'status':status.HTTP_403_FORBIDDEN})
        
        # Find employee to delete
        queryset = Employee.objects.all()
        fired_employee = get_object_or_404(queryset, pk=pk)

        # Cannot delete own self
        if fired_employee is employee:
            return Response({'status':status.HTTP_403_FORBIDDEN})

        # Cannot delete staff
        if fired_employee.user.is_staff:
            return Response({'status':status.HTTP_403_FORBIDDEN})

        # Only staff can delete owners
        if fired_employee.role is settings.EMPLOYEE_OWNER_ROLE:
            if employee.user.is_staff():
                fired_employee.delete()
                return Response({'status':status.HTTP_200_OK})
            else:
                return Response({'status':status.HTTP_403_FORBIDDEN})

        # Staff can delete no problem, but non-staff have to ensure
        # they belong in the same organization.
        if employee.is_staff:
            fired_employee.delete()
            return Response({'status':status.HTTP_200_OK})
        else:
            if fired_employee.organization is not employee.organization:
                return Response({'status':status.HTTP_403_FORBIDDEN})
            else:
                fired_employee.delete()
                return Response({'status':status.HTTP_200_OK})
