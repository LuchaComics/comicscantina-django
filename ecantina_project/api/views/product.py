import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import TinyResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly
from api.serializers import ProductSerializer
from api.models.ec.product import Product
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee


class ProductFilter(django_filters.FilterSet):
    brand_name = django_filters.CharFilter(name="brand__name", lookup_type=("icontains"))
    tag = django_filters.CharFilter(name="tag__name", lookup_type=("icontains"))
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    organization = django_filters.CharFilter(name="organization__org_id")
    store = django_filters.CharFilter(name="store__store_id")
    section = django_filters.CharFilter(name="section__section_id")
    category = django_filters.CharFilter(name="category__category_id")
    category_name = django_filters.CharFilter(name="category__name", lookup_type=("icontains"))
    min_sub_price = django_filters.CharFilter(name="sub_price", lookup_type=("gte"))
    max_sub_price = django_filters.CharFilter(name="sub_price", lookup_type=("lte"))
    min_price = django_filters.CharFilter(name="price", lookup_type=("gte"))
    max_price = django_filters.CharFilter(name="price", lookup_type=("lte"))
    min_discount = django_filters.CharFilter(name="discount", lookup_type=("gte"))
    store_aggregated_listing = django_filters.BooleanFilter(name="store__is_aggregated")
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'description', 'type', 'created', 'last_updated', 'is_sold', 'sub_price', 'discount', 'discount_type', 'price', 'cost', 'image', 'image_url', 'organization', 'store', 'section', 'brand', 'brand_name', 'tag', 'is_available', 'category', 'category_name', 'min_sub_price', 'max_sub_price', 'min_price', 'max_price', 'min_discount', 'is_new', 'is_featured', 'is_qrcode_printed', 'language', 'currency', 'store_aggregated_listing',]


class ProductViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = TinyResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter


