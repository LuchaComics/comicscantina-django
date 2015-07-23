from api.permissions import IsEmployeeUser
from api.models.ec.employee import Employee
from api.serializers import EmployeeSerializer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class EmployeeList(generics.ListCreateAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    
    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        return Employee.objects.filter(organization=employee.organization)

class EmployeeDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer