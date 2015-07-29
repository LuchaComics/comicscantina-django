from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser
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
    permission_classes = (IsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=product_id',)

    def list(self, request):
        employee = Employee.objects.get(user=self.request.user)
        products = Product.objects.filter(comic__organization=employee.organization)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
