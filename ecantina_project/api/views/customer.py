from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.permissions import IsEmployeeUser
from api.serializers import CustomerSerializer
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee

class CustomerViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (IsEmployeeUser, IsAuthenticated)
