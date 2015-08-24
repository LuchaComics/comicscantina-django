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
from api.models.gcd.series import Series
from api.models.gcd.issue import Issue
from api.models.gcd.storytype import GCDStoryType
from api.models.gcd.story import GCDStory
from api.models.gcd.branduse import GCDBrandUse
from api.models.gcd.brandemblemgroup import GCDBrandEmblemGroup

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
admin.site.register(GCDCountry)
admin.site.register(GCDLanguage)
admin.site.register(GCDImage)
admin.site.register(GCDIndiciaPublisher)
admin.site.register(GCDBrandGroup)
admin.site.register(GCDBrand)
admin.site.register(Series)
admin.site.register(Issue)
admin.site.register(GCDStoryType)
admin.site.register(GCDStory)
admin.site.register(GCDBrandUse)
admin.site.register(GCDBrandEmblemGroup)
# EC
admin.site.register(Comic)
admin.site.register(Customer)
admin.site.register(Employee)
admin.site.register(HelpRequest)
admin.site.register(ImageUpload)
admin.site.register(Organization)
admin.site.register(Section)
admin.site.register(Store)
