import django_filters
from datetime import datetime
from decimal import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from rest_framework.decorators import detail_route
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.receipt import Receipt
from api.serializers import ReceiptSerializer


class ReceiptFilter(django_filters.FilterSet):
    has_finished = django_filters.BooleanFilter(name="has_finished")
    class Meta:
        model = Receipt
        fields = ['organization', 'store', 'customer', 'has_finished', 'status', 'has_error', 'error', 'has_purchased_online','employee',]


class ReceiptViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    search_fields = ('billing_name','email','billing_phone','billing_postal','shipping_name', 'shipping_phone','shipping_postal',)
    filter_class = ReceiptFilter

  
    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_checkout_computation(self, request, pk=None):
        #
        # Note: For more information on setting up custom functions, see this url:
        # http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
        #
        receipt = self.get_object() # Fetch the receipt we will be processing.
        
        # Iterate through all the products and compute the total receipt amount.
        self.process_receipt(receipt)
        
        # Return success message.
        return Response({'status': 'Receipt updated'})

    def process_receipt(self, receipt):
        """
            Helper function used to compute the totals
        """
        # Iterate through all the products and create a calculate
        # our totals.
        sub_tota_amount = Decimal(0.00)
        total_discount_amount = Decimal(0.00)
        total_tax_amount = Decimal(0.00)
        total_amount = Decimal(0.00)
        for product in receipt.products.all():
            # Process discount
            if product.discount_type is 1: # Percent
                rate = Decimal(product.discount) / Decimal(100)
                discount_amount = Decimal(rate) * Decimal(product.sub_price)
            elif product.discount_type is 2: # Amount
                discount_amount =  product.discount
            post_discount_price = product.sub_price - discount_amount
            total_discount_amount += discount_amount
                    
            # Process sub-amount
            sub_tota_amount += post_discount_price
                    
            # Process tax
            if receipt.has_tax:
                tax_rate = Decimal(0.13)
                tax_amount = post_discount_price * tax_rate
                total_tax_amount += tax_amount
    
            # Process total amount
            total_amount += post_discount_price + tax_amount
            
        # Update financial
        receipt.sub_total = sub_tota_amount
        receipt.discount_amount = total_discount_amount
        receipt.tax_amount = total_tax_amount
        receipt.total_amount = total_amount
        receipt.save()
