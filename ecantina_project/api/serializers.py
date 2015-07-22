from django.forms import widgets
from rest_framework import serializers
from api.models.ec.customer import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'joined', 'last_updated', 'first_name', 'last_name', 'email', 'phone', 'street_name', 'street_number', 'unit_number', 'province', 'country', 'postal', 'has_consented', 'user', 'profile',)