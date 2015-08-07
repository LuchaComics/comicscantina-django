from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser, IsEmployeeMemberOfOrganization
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.cart import Cart
from api.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsEmployeeUser, IsEmployeeMemberOfOrganization, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('is_closed','customer','employee',)

