from django.contrib import admin

# Grand Comics Database Models
#------------------------------------------------------------------
from inventory.models.gcd.country import Country
from inventory.models.gcd.language import Language
from inventory.models.gcd.image import Image
from inventory.models.gcd.indiciapublisher import IndiciaPublisher
from inventory.models.gcd.publisher import Publisher
from inventory.models.gcd.brandgroup import BrandGroup
from inventory.models.gcd.brand import Brand
from inventory.models.gcd.series import Series
from inventory.models.gcd.issue import Issue
from inventory.models.gcd.storytype import StoryType
from inventory.models.gcd.story import Story
from inventory.models.gcd.branduse import BrandUse
from inventory.models.gcd.brandemblemgroup import BrandEmblemGroup

# Comics Cantina Database Models
#------------------------------------------------------------------
from inventory.models.ec.store import Store
from inventory.models.ec.employee import Employee
from inventory.models.ec.location import Location
from inventory.models.ec.comic import Comic

# Registering Models
#------------------------------------------------------------------
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
admin.site.register(Store)
admin.site.register(Employee)
admin.site.register(Location)
admin.site.register(Comic)
