import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import UnifiedShippingRateSerializer
from api.models.ec.unified_shipping_rates import UnifiedShippingRate


class UnifiedShippingRateFilter(django_filters.FilterSet):
    class Meta:
        model = UnifiedShippingRate
        fields = ['country',]


class UnifiedShippingRateViewSet(viewsets.ModelViewSet):
    queryset = UnifiedShippingRate.objects.all()
    serializer_class = UnifiedShippingRateSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_class = UnifiedShippingRateFilter