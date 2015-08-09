from django.forms import widgets
from rest_framework import serializers
from api.models.ec.cart import Cart
from api.models.ec.customer import Customer
from api.models.ec.product import Product
from api.models.ec.employee import Employee
from api.models.ec.comic import Comic
from api.models.ec.purchase import Purchase
from api.models.ec.receipt import Receipt

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'joined', 'last_updated', 'first_name', 'last_name', 'email', 'phone', 'street_name', 'street_number', 'unit_number', 'province', 'country', 'postal', 'has_consented', 'user', 'profile',)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('customer', 'employee', 'products', 'cart_id', 'created', 'last_updated', 'is_closed','has_tax',)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('product_id', 'name', 'type', 'created', 'last_updated', 'is_sold', 'sub_price', 'discount', 'discount_type', 'price', 'cost', 'image', 'images', 'organization', 'store', 'section',)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_id', 'role',  'joined', 'last_updated', 'email', 'phone', 'street_name', 'street_number', 'unit_number', 'province', 'country', 'postal', 'user', 'organization', 'profile',)

class ComicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comic
        fields = ('comic_id', 'is_cgc_rated', 'age',
                  'cgc_rating', 'label_colour', 'condition_rating', 'is_canadian_priced_variant', 'is_variant_cover', 'is_retail_incentive_variant', 'is_newsstand_edition', 'issue',
                  )

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ('customer', 'product', 'purchase_id', 'purchased_date', 'sub_amount', 'discount_amount', 'tax_amount', 'amount', 'organization',)

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('organization','store','customer','receipt_id','purchased_date','type','payment_method','has_custom_billing_address','first_name','last_name','email','phone','street_name','street_number','unit_number','city','province','country','postal','purchases','sub_total','tax_amount','total_amount',)