from api.models.ec.cart import Cart
from api.serializers import CartSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import permissions
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee


class CartList(APIView):
    """
        List all carts, or create a new cart.
    """
    permission_classes = (permissions.IsEmployee, )
    
    def get(self, request, format=None):
        employee = Employee.objects.get(user=request.user)
        carts = Cart.objects.filter(employee=employee)
        carts = carts.filter(is_closed=False).order_by("-created")
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CartDetail(APIView):
    """
        Retrieve, update or delete a cart instance.
    """
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        cart = self.get_object(pk)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)