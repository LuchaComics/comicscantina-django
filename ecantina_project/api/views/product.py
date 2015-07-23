from api.permissions import IsEmployeeUser
from api.models.ec.product import Product
from api.serializers import ProductSerializer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class ProductList(generics.ListCreateAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        return Product.objects.filter(comic__organization=employee.organization)

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer