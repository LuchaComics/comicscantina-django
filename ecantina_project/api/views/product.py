from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser, IsOnlyOwnedByOrganization
from api.serializers import ProductSerializer
from api.models.ec.product import Product
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee

class ProductViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsEmployeeUser, IsOnlyOwnedByOrganization, IsAuthenticated)
    filter_backends = (filters.DjangoFilterBackend,)
#    filter_fields = ('product_id',)