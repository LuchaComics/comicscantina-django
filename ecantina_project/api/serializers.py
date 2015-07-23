from django.forms import widgets
from rest_framework import serializers
from api.models.ec.cart import Cart
from api.models.ec.customer import Customer
from api.models.ec.product import Product
from api.models.ec.employee import Employee

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'joined', 'last_updated', 'first_name', 'last_name', 'email', 'phone', 'street_name', 'street_number', 'unit_number', 'province', 'country', 'postal', 'has_consented', 'user', 'profile',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('customer', 'employee', 'products', 'cart_id', 'created', 'last_updated', 'is_closed',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'type', 'comic',)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_id', 'role',  'joined', 'last_updated', 'email', 'phone', 'street_name', 'street_number', 'unit_number', 'province', 'country', 'postal', 'user', 'organization', 'profile',)


#{
#    "customer": null,
#    "employee": null,
#    "products": [],
#    "is_closed": false
#}