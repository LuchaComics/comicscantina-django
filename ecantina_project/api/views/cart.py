from api.permissions import IsEmployeeUser
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.cart import Cart
from api.serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics


class CartList(generics.ListCreateAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        employee = Employee.objects.get(user=self.request.user)
        carts = Cart.objects.filter(employee=employee)
        return carts.filter(is_closed=False).order_by("-created")


class CartDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsEmployeeUser, IsAuthenticated )
    queryset = Cart.objects.all()
    serializer_class = CartSerializer