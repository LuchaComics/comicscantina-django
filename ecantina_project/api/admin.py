from django.contrib import admin

# Grand Comics Database Models
#------------------------------------------------------------------
from api.models.gcd.country import GCDCountry
from api.models.gcd.language import GCDLanguage
from api.models.gcd.image import GCDImage
from api.models.gcd.indiciapublisher import GCDIndiciaPublisher
from api.models.gcd.publisher import GCDPublisher
from api.models.gcd.brandgroup import GCDBrandGroup
from api.models.gcd.brand import GCDBrand
from api.models.gcd.series import GCDSeries
from api.models.gcd.issue import GCDIssue
from api.models.gcd.storytype import GCDStoryType
from api.models.gcd.story import GCDStory
from api.models.gcd.branduse import GCDBrandUse
from api.models.gcd.brandemblemgroup import GCDBrandEmblemGroup

# Comics Cantina Database Models
#------------------------------------------------------------------
from api.models.ec.brand import Brand
from api.models.ec.category import Category
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.helprequest import HelpRequest
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.product import Product
from api.models.ec.promotion import Promotion
from api.models.ec.pulllist import Pulllist
from api.models.ec.pulllistsubscription import PulllistSubscription
from api.models.ec.receipt import Receipt
from api.models.ec.section import Section
from api.models.ec.store import Store
from api.models.ec.tag import Tag
from api.models.ec.wishlist import Wishlist
from api.models.ec.orgshippingpreference import OrgShippingPreference
from api.models.ec.orgshippingrate import OrgShippingRate
from api.models.ec.store_shipping_preference import StoreShippingPreference
from api.models.ec.store_shipping_rates import StoreShippingRate
from api.models.ec.emailsubscription import EmailSubscription


# Registering Models
#------------------------------------------------------------------
# GCD
admin.site.register(GCDCountry)
admin.site.register(GCDLanguage)
admin.site.register(GCDImage)
admin.site.register(GCDIndiciaPublisher)
admin.site.register(GCDBrandGroup)
admin.site.register(GCDBrand)
admin.site.register(GCDSeries)
admin.site.register(GCDIssue)
admin.site.register(GCDStoryType)
admin.site.register(GCDStory)
admin.site.register(GCDBrandUse)
admin.site.register(GCDBrandEmblemGroup)
# EC
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(Comic)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(HelpRequest)
admin.site.register(ImageUpload)
admin.site.register(Organization)
admin.site.register(Product)
admin.site.register(Promotion)
admin.site.register(Pulllist)
admin.site.register(PulllistSubscription)
admin.site.register(Receipt)
admin.site.register(Section)
admin.site.register(Store)
admin.site.register(Tag)
admin.site.register(Wishlist)
admin.site.register(OrgShippingPreference)
admin.site.register(OrgShippingRate)
admin.site.register(StoreShippingPreference)
admin.site.register(StoreShippingRate)
admin.site.register(EmailSubscription)
