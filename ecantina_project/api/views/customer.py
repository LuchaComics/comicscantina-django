import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.serializers import CustomerSerializer
from api.models.ec.customer import Customer
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee


class CustomerFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(name="first_name", lookup_type=("icontains"))
    last_name = django_filters.CharFilter(name="last_name", lookup_type=("icontains"))
    email = django_filters.CharFilter(name="email", lookup_type=("icontains"))
    phone = django_filters.CharFilter(name="billing_phone", lookup_type=("icontains"))
    postal = django_filters.CharFilter(name="billing_postal", lookup_type=("icontains"))
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'postal', 'is_suspended',]


class CustomerViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = (BelongsToCustomerOrIsEmployeeUser,)
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    search_fields = ('=customer_id', 'first_name', 'last_name', 'email')
    filter_class = CustomerFilter