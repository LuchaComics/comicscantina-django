from django.forms import widgets
from django.contrib.auth.models import User, Group
from rest_framework import serializers
from api.models.ec.customer import Customer
from api.models.ec.store import Store
from api.models.ec.organization import Organization
from api.models.ec.product import Product
from api.models.ec.employee import Employee
from api.models.ec.comic import Comic
from api.models.ec.receipt import Receipt
from api.models.ec.helprequest import HelpRequest
from api.models.ec.imageupload import ImageUpload
from api.models.ec.promotion import Promotion
from api.models.ec.section import Section
from api.models.ec.wishlist import Wishlist
from api.models.ec.pulllist import Pulllist


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('customer_id', 'joined', 'last_updated', 'first_name', 'last_name', 'email', 'billing_name', 'billing_phone', 'billing_street_name', 'billing_street_number', 'billing_unit_number', 'billing_city', 'billing_province', 'billing_country', 'billing_postal', 'shipping_name', 'shipping_phone', 'shipping_street_name', 'shipping_street_number', 'shipping_unit_number', 'shipping_city', 'shipping_province', 'shipping_country', 'shipping_postal', 'has_consented', 'user', 'profile',)

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_id', 'name', 'description', 'joined', 'last_updated', 'street_name', 'street_number', 'unit_number', 'city', 'province', 'country', 'postal', 'website', 'email', 'phone', 'fax', 'is_open_monday', 'is_open_tuesday', 'is_open_wednesday', 'is_open_thursday', 'is_open_friday', 'is_open_saturday', 'is_open_sunday', 'monday_to', 'tuesday_to', 'wednesday_to', 'thursday_to', 'friday_to', 'saturday_to', 'sunday_to', 'monday_from', 'tuesday_from', 'wednesday_from', 'thursday_from', 'friday_from', 'saturday_from', 'sunday_from', 'organization', 'employees', 'logo', 'tax_rate',)


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ('org_id', 'name', 'description', 'joined', 'last_updated', 'street_name', 'street_number', 'unit_number', 'city', 'province', 'country', 'postal', 'website', 'email', 'phone', 'fax', 'twitter_url', 'facebook_url', 'instagram_url', 'linkedin_url', 'github_url', 'google_url', 'youtube_url', 'flickr_url', 'administrator', 'logo','customers',)


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


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ('organization','store','employee','customer','receipt_id','created','last_updated','has_purchased_online','payment_method','products','sub_total', 'discount_amount', 'has_tax', 'tax_rate', 'tax_amount','total_amount', 'has_finished', 'has_paid', 'status', 'billing_first_name', 'billing_last_name', 'billing_address', 'billing_email', 'billing_phone', 'billing_city', 'billing_province', 'billing_country', 'billing_postal','shipping_first_name', 'shipping_last_name', 'shipping_address', 'shipping_email', 'shipping_phone', 'shipping_city', 'shipping_province', 'shipping_country', 'shipping_postal',)


class HelpRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HelpRequest
        fields = ('help_id', 'subject', 'subject_url', 'message', 'submission_date', 'screenshot', 'employee', 'store', 'organization',)


class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageUpload
        fields = ('upload_id', 'upload_date', 'is_assigned', 'image', 'user',)


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ('promotion_id', 'name', 'discount', 'discount_type', 'organization',)


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('section_id', 'name', 'store', 'organization')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('wishlist_id', 'customer', 'products')


class PulllistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pulllist
        fields = ('pulllist_id', 'organization', 'series', 'customers',)
