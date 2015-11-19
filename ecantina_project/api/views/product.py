from decimal import *
import django_filters
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import filters
from rest_framework.decorators import detail_route
from api.pagination import TinyResultsSetPagination
from api.permissions import BelongsToOrganizationOrReadOnly, BelongsToCustomerOrIsEmployeeUser
from api.serializers import ProductSerializer
from api.models.ec.product import Product
from api.models.ec.promotion import Promotion
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
        fields = ['product_id', 'name', 'description', 'type', 'created', 'last_updated', 'is_sold', 'sub_price', 'discount', 'discount_type', 'price', 'cost', 'image', 'organization', 'store', 'section', 'brand', 'brand_name', 'tag', 'is_available', 'category', 'category_name', 'min_sub_price', 'max_sub_price', 'min_price', 'max_price', 'min_discount', 'is_new', 'is_featured', 'is_qrcode_printed', 'language', 'currency', 'store_aggregated_listing',]


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

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def apply_tax_and_discounts(self, request, pk=None):
        """
            Function will add discounts and taxes to the product.
        """
        product = self.get_object() # Fetch the product we will be processing.

        try:
            promotions = Promotion.objects.filter(organization=product.organization)
        except Promotion.DoesNotExist:
            Promotions = None

        if product.store.tax_rate > 0:
            product.tax_rate = product.store.tax_rate
            product.tax_amount = product.sub_price * product.tax_rate
            product.sub_price_with_tax = product.tax_amount + product.sub_price
            
        # Iterate through all the Tags and sum their discounts
        total_percent = Decimal(0.00)
        total_amount = Decimal(0.00)
        for tag in product.tags.all():
            if tag.discount_type is 1:
                total_percent += tag.discount
            if tag.discount_type is 2:
                total_amount += tag.discount
        
        # Iterate through all the Promotions and sum their discounts.
        for promotion in promotions:
            if promotion.discount_type is 1:
                total_percent += promotion.discount
            if promotion.discount_type is 2:
                total_amount += promotion.discount
            
        # Compute the discount
        if total_percent > 0:
            product.discount = product.sub_price_with_tax * (total_percent/100)
                    
            if total_amount > 0:
                product.discount += total_amount
                    
            if total_percent > 0 or total_amount > 0:
                product.discount_type = 2
                
        # Compute final price.
        product.price = (product.sub_price_with_tax - product.discount)
        product.save()

        return Response({'status': 'success', 'message': 'discounts and taxes successfully applied'})
