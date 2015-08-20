import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsAdminUserOrReadOnly
from api.models.gcd.series import Series
from api.serializers import SeriesSerializer
from rest_framework.pagination import PageNumberPagination


class SeriesFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    publisher_name = django_filters.CharFilter(name="publisher__name", lookup_type=("icontains"))
    min_year_began = django_filters.NumberFilter(name="year_began", lookup_type='gte')
    max_year_ended = django_filters.NumberFilter(name="year_ended", lookup_type='lte')
    class Meta:
        model = Series
        fields = ['name', 'publisher_name', 'min_year_began', 'max_year_ended', 'language', 'country',]


class SeriesViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Series.objects.all()
    serializer_class = SeriesSerializer
    permission_classes = (IsAdminUserOrReadOnly, IsAuthenticated)
    pagination_class = LargeResultsSetPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = SeriesFilter
