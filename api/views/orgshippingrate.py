import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import OrgShippingRateSerializer
from api.models.ec.orgshippingrate import OrgShippingRate


class OrgShippingRateFilter(django_filters.FilterSet):
    class Meta:
        model = OrgShippingRate
        fields = ['organization','country',]


class OrgShippingRateViewSet(viewsets.ModelViewSet):
    queryset = OrgShippingRate.objects.all()
    serializer_class = OrgShippingRateSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_class = OrgShippingRateFilter