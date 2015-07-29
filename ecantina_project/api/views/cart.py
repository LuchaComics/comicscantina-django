from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.permissions import IsEmployeeUser
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
    permission_classes = (IsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=employee__employee_id', '=cart_id')

    def list(self, request):
        employee = Employee.objects.get(user=self.request.user)
        carts = Cart.objects.filter(employee=employee)
        carts = carts.filter(is_closed=False).order_by("-created")
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)