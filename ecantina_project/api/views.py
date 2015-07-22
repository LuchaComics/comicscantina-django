from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import CustomerSerializer
from api.models.ec.customer import Customer

class CustomerViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows users to be viewed or edited.
        """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
