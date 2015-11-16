import django_filters
from datetime import datetime
from decimal import *
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import filters
from rest_framework.decorators import detail_route
from ecantina_project import constants
from api.pagination import LargeResultsSetPagination
from api.permissions import BelongsToCustomerOrIsEmployeeUser
from api.models.ec.organization import Organization
from api.models.ec.employee import Employee
from api.models.ec.customer import Customer
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.receipt import Receipt
from api.models.ec.promotion import Promotion
from api.models.ec.unified_shipping_rates import UnifiedShippingRate
from api.serializers import ReceiptSerializer


class ReceiptFilter(django_filters.FilterSet):
    has_finished = django_filters.BooleanFilter(name="has_finished")
    class Meta:
        model = Receipt
        fields = ['receipt_id', 'organization', 'store', 'customer', 'has_finished', 'status', 'has_error', 'error', 'has_purchased_online','employee', 'has_shipping',]


class ReceiptViewSet(viewsets.ModelViewSet):
    """
        API endpoint that allows customers to be viewed or edited.
    """
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer
    pagination_class = LargeResultsSetPagination
    permission_classes = (BelongsToCustomerOrIsEmployeeUser, IsAuthenticated)
    filter_backends = (filters.SearchFilter,filters.DjangoFilterBackend,)
    search_fields = ('email','billing_phone','billing_postal', 'shipping_phone','shipping_postal',)
    filter_class = ReceiptFilter
  
    def get_customer_receipts(self, user_id):
        """
            HELPER FUNCTION: Used to return all the Receipt(s) that belong to 
            the Customer User in our system.
        """
        try:
            customer = Customer.objects.filter(user_id=user_id)
            receipt = Receipt.objects.filter(customer=customer)
            return receipt
        except Customer.DoesNotExist:
            return Receipt.objects.none()

    def get_queryset(self):
        """
            SECURITY: The following query override was set to protect private
            Customer information from being leaked to non-employee staff.
        """
        # If user is an Employee then they have permission to list all the
        # Customers Receipts in our application that belong to the organization,
        # else don't show.
        try:
            employee = Employee.objects.get(user__id=self.request.user.id)
            receipt = Receipt.objects.filter(organization=employee.organization)
            # If no receipts where returned, then return the customer receipt.
            if len(receipt) is 0:
                return self.get_customer_receipts(self.request.user.id)
            else:
                return receipt
        except Employee.DoesNotExist:
            return self.get_customer_receipts(self.request.user.id)
        except Receipt.DoesNotExist:
            return Receipt.objects.none() # Worst Case: Return nothing found.
  
    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def apply_discounts(self, request, pk=None):
        """
            Function will iterate through all the products in the cart and
            apply the associated Tag & Promotion discounts per each product.
            Afterwords, each product will have the latest up-to-date price
            associated with the current discounts.
        """
        receipt = self.get_object() # Fetch the receipt we will be processing.
        try:
            promotions = Promotion.objects.filter(organization=receipt.organization)
        except Promotion.DoesNotExist:
            Promotions = None

        for product in receipt.products.all():
            # SECURIY: Ensure the appropriate taxes are applied from the store.
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

        return Response({'status': 'success', 'message': 'discounts successfully applied'})

  
    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_tally(self, request, pk=None):
        """
            Function will find the total amount that is owed for the bill and
            save it in the receipt.
        """
        receipt = self.get_object() # Fetch the receipt we will be processing.
        self.tally_up_receipt(receipt)
        return Response({'status': 'success', 'message': 'tallied up totals'})

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_verification(self, request, pk=None):
        """
            Function will verify that the products being checked out are 
            available and can be checked out. If any problems arise this
            function will return a failed message.
        """
        receipt = self.get_object() # Fetch the receipt we will be processing.
        message = self.verify(receipt)
        if message:
            return message
        else:
            return Response({'status': 'success', 'message': 'is ready for checkout'})

    @detail_route(methods=['get'], permission_classes=[BelongsToCustomerOrIsEmployeeUser])
    def perform_checkout(self, request, pk=None):
        """
            Function will be used by in-store staff / point of sale device
            to perform transaction handling.
        """
        receipt = self.get_object() # Fetch the receipt we will be processing.
        
        # STEP 1: Verify that our cart can be checked out.
        message = self.verify(receipt)
        if message:
            return message
        if receipt.employee is None:
            return Response({'status': 'failed', 'message': 'must belong to employee'})

        # STEP 2: Compute the final bill
        self.tally_up_receipt(receipt)

        # STEP 3: Set our customer information to the receipt if not guest shopper.
        if receipt.customer:
            billing_address = receipt.customer.billing_street_number
            billing_address += ' ' + receipt.customer.billing_street_name
            if receipt.customer.billing_unit_number:
                billing_address = receipt.customer.billing_unit_number + '-' + billing_address

            shipping_address = receipt.customer.shipping_street_number
            shipping_address += ' ' + receipt.customer.shipping_street_name
            if receipt.customer.shipping_unit_number:
                shipping_address = receipt.customer.shipping_unit_number + '-' + shipping_address

            receipt.email = receipt.customer.email
            receipt.billing_address = billing_address
            receipt.billing_phone = receipt.customer.billing_phone
            receipt.billing_city = receipt.customer.billing_city
            receipt.billing_province = receipt.customer.billing_province
            receipt.billing_country = receipt.customer.billing_country
            receipt.billing_postal = receipt.customer.billing_postal
            receipt.shipping_address = shipping_address
            receipt.shipping_phone = receipt.customer.shipping_phone
            receipt.shipping_city = receipt.customer.shipping_city
            receipt.shipping_province = receipt.customer.shipping_province
            receipt.shipping_country = receipt.customer.shipping_country
            receipt.shipping_postal = receipt.customer.shipping_postal

        # STEP 3: Finalize our receipt.
        receipt.purchased = datetime.today()
        receipt.has_finished = True
        receipt.has_paid = True
        receipt.status = constants.IN_STORE_SALE_STATUS
        receipt.payment_method = constants.CASH_PAYMENT_METHOD
        receipt.save()
        
        # STEP 4: Inform our products that they are sold out.
        for product in receipt.products.all():
            product.is_sold = True
            product.save()

        return Response({'status': 'success', 'message': 'checkout complete'})

    def verify(self, receipt):
        # Verify Receipt.
        if receipt.has_paid:
            return Response({'status': 'failed', 'message': 'customer has already paid for receipt' })
        if receipt.has_finished:
            return Response({'status': 'failed', 'message': 'receipt has already been finsihed' })
        
        # Verify Products.
        for product in receipt.products.all():
            if product.is_sold:
                return Response({'status': 'failed', 'message': 'product was already sold: '+product.name })
            if product.is_available is False:
                return Response({'status': 'failed', 'message': 'product is no longer sold: '+product.name })
        return None

    def tally_up_receipt(self, receipt):
        """
            Helper function used to compute the totals
        """
        # Iterate through all the products and create a calculate our totals.
        tax_rates = list()
        sub_total_amount = Decimal(0.00)
        total_tax_amount = Decimal(0.00)
        sub_total_amount_with_tax = Decimal(0.00)
        total_discount_amount = Decimal(0.00)
        for product in receipt.products.all():
            # Sub Price
            sub_total_amount += product.sub_price
            
            # Tax
            if product.has_tax:
                tax_rates.append(product.tax_rate)
                total_tax_amount += product.tax_amount
            else:
                tax_rates.append(0)
            
            # Sub Price + Tax
            sub_total_amount_with_tax += product.sub_price_with_tax
            
            # Discounts
            if product.discount > 0:
                if product.discount_type is 1: # Percent
                    rate = Decimal(product.discount) / Decimal(100)
                    discount_amount = Decimal(rate) * Decimal(product.sub_price_with_tax)
                elif product.discount_type is 2: # Amount
                    discount_amount =  product.discount
                total_discount_amount += discount_amount
    
        # Calculate tax
        if len(tax_rates) > 0:
            avg_tax_rate = sum(tax_rates)/len(tax_rates)
            has_tax = avg_tax_rate > 0
        else:
            avg_tax_rate = Decimal(0.00)
            has_tax = False
    
        # Calculate shipping for the specific organization.
        shipping_amount = 0
        if receipt.has_purchased_online:
            if receipt.has_shipping:
                shipping_amount = self.compute_shipping_cost(receipt)

        # Update financials.
        receipt.sub_total = sub_total_amount
        receipt.has_tax = has_tax
        receipt.tax_rate = avg_tax_rate
        receipt.tax_amount = total_tax_amount
        receipt.sub_total_with_tax = sub_total_amount_with_tax
        receipt.discount_amount = total_discount_amount
        receipt.shipping_amount = shipping_amount
        receipt.total_amount = sub_total_amount_with_tax
        receipt.total_amount -= total_discount_amount
        receipt.total_amount += shipping_amount
        receipt.save()

    def compute_shipping_cost(self, receipt):
        # CASE 1: We have a single organization that receipt belongs to.
        if receipt.organization:
            # Fetch the organization preferences on how to handle shipping rates.
            preference = OrgShippingPreference.objects.get(organization=receipt.organization)
            
            # If the organization set to in-store pickup only, then return zero
            # shipping costs as the cost of travelling to store is handled by
            # customer in real life.
            if preference.is_pickup_only:
                return Decimal(0.00)
    
            # Determine where the receipt is to be shipped
            iso_3166_1_numeric_country_code = 0
            if 'Canada' in receipt.shipping_country:
                iso_3166_1_numeric_country_code = 124
            elif 'United States' in receipt.shipping_country:
                iso_3166_1_numeric_country_code = 840
            elif 'Mexico' in receipt.shipping_country:
                iso_3166_1_numeric_country_code = 484

            # Find the shipping rate to apply for the country and apply it.
            for rate in preference.rates.all():
                if rate.country is iso_3166_1_numeric_country_code:
                    # Count how many products we are to ship and apply the
                    # appropriate shipping rates. Note: These rates where taken
                    # from the following file:
                    # - - - - - - - - - - - - - - - - - - - - - - - - -
                    # inventory_settings/forms/org_shipping_rates_form
                    # - - - - - - - - - - - - - - - - - - - - - - - - -
                    comics_count = len(receipt.products.all())
                    return rate.get_comics_rate(comics_count)
                                        
        # CASE 2: We have no organization.
        else:
            # Determine where the receipt is to be shipped.
            iso_3166_1_numeric_country_code = 0
            if 'Canada' in receipt.shipping_country:
                iso_3166_1_numeric_country_code = 124
            elif 'United States' in receipt.shipping_country:
                iso_3166_1_numeric_country_code = 840
            elif 'Mexico' in receipt.shipping_country:
                iso_3166_1_numeric_country_code = 484

            # Find the rate.
            try:
                rate = UnifiedShippingRate.objects.get(country=iso_3166_1_numeric_country_code)
                comics_count = len(receipt.products.all())
                return rate.get_comics_rate(comics_count)
            except UnifiedShippingRate.DoesNotExist:
                # Add "Shipping Rate Error" to our cart.
                receipt.has_error = True
                receipt.error = constants.SHIPPING_RATE_ERROR_TYPE
                receipt.save()
            
        return Decimal(0.00) # Case 3: Nothing was found.

#
# Note: For more information on setting up custom functions, see this url:
# http://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing
#