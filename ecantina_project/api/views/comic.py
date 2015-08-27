import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import IsEmployeeUser
from api.serializers import ComicSerializer
from api.models.ec.comic import Comic
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee


class ComicFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(name="product__product_id")
    issue = django_filters.CharFilter(name="issue__issue_id")
    is_newsstand_edition = django_filters.BooleanFilter(name="is_newsstand_edition")
    is_retail_incentive_variant = django_filters.BooleanFilter(name="is_retail_incentive_variant")
    is_variant_cover = django_filters.BooleanFilter(name="is_variant_cover")
    is_canadian_priced_variant = django_filters.BooleanFilter(name="is_canadian_priced_variant")
    class Meta:
        model = Comic
        fields = ['comic_id', 'is_cgc_rated', 'age', 'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', 'issue', 'product',]


class ComicViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (IsEmployeeUser, IsAuthenticated)
    filter_class = ComicFilter