from django.contrib import admin

# Grand Comics Database Models
#------------------------------------------------------------------
from api.models.gcd.country import Country
from api.models.gcd.language import Language
from api.models.gcd.image import Image
from api.models.gcd.indiciapublisher import IndiciaPublisher
from api.models.gcd.publisher import Publisher
from api.models.gcd.brandgroup import BrandGroup
from api.models.gcd.brand import Brand
from api.models.gcd.series import Series
from api.models.gcd.issue import Issue
from api.models.gcd.storytype import StoryType
from api.models.gcd.story import Story
from api.models.gcd.branduse import BrandUse
from api.models.gcd.brandemblemgroup import BrandEmblemGroup

# Comics Cantina Database Models
#------------------------------------------------------------------
from api.models.ec.comic import Comic
from api.models.ec.customer import Customer
from api.models.ec.employee import Employee
from api.models.ec.helprequest import HelpRequest
from api.models.ec.imageupload import ImageUpload
from api.models.ec.organization import Organization
from api.models.ec.section import Section
from api.models.ec.store import Store


# Registering Models
#------------------------------------------------------------------
# GCD
admin.site.register(Country)
admin.site.register(Language)
admin.site.register(Image)
admin.site.register(IndiciaPublisher)
admin.site.register(BrandGroup)
admin.site.register(Brand)
admin.site.register(Series)
admin.site.register(Issue)
admin.site.register(StoryType)
admin.site.register(Story)
admin.site.register(BrandUse)
admin.site.register(BrandEmblemGroup)
# EC
admin.site.register(Comic)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(HelpRequest)
admin.site.register(ImageUpload)
admin.site.register(Organization)
admin.site.register(Section)
admin.site.register(Store)
