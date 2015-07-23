from api.permissions import IsEmployeeUser
from api.models.ec.customer import Customer
from api.serializers import CustomerSerializer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    serializer_class = CustomerSerializer

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer