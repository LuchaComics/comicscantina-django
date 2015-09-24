import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly
from api.serializers import ProductSerializer
from api.models.ec.product import Product
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee


class ProductFilter(django_filters.FilterSet):
    brand_name = django_filters.CharFilter(name="brand__brand_name", lookup_type=("icontains"))
    tag = django_filters.CharFilter(name="tag__tag_name", lookup_type=("icontains"))
    name = django_filters.CharFilter(name="name", lookup_type=("icontains"))
    organization = django_filters.CharFilter(name="organization__organization_id")
    store = django_filters.CharFilter(name="store__store_id")
    section = django_filters.CharFilter(name="section__section_id")
    category = django_filters.CharFilter(name="category__category_id")
    category_name = django_filters.CharFilter(name="category__category_name", lookup_type=("icontains"))
    min_price = django_filters.CharFilter(name="price", lookup_type=("gte"))
    max_price = django_filters.CharFilter(name="price", lookup_type=("lte"))
    class Meta:
        model = Product
        fields = ['product_id', 'name', 'type', 'created', 'last_updated', 'is_sold', 'sub_price', 'discount', 'discount_type', 'price', 'cost', 'image', 'image_url', 'organization', 'store', 'section', 'brand', 'brand_name', 'tag', 'is_available', 'category', 'category_name', 'min_price', 'max_price', 'is_new', 'is_featured', 'is_qrcode_printed', 'language', 'currency',]


class ProductViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToOrganizationOrReadOnly, IsAuthenticatedOrReadOnly)
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = ProductFilter


