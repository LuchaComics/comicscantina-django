from django.conf.urls import url, include
from api.views import comic
from api.views import customer
from api.views import organization
from api.views import store
from api.views import product
from api.views import employee
from api.views import receipt
from api.views import helprequest
from api.views import imageupload
from api.views import promotion
from api.views import section
from api.views import user
from api.views import wishlist
from api.views import pulllist
from api.views import pulllistsubscription
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'comics', comic.ComicViewSet)
router.register(r'organizations', organization.OrganizationViewSet)
router.register(r'customers', customer.CustomerViewSet)
router.register(r'stores', store.StoreViewSet)
router.register(r'products', product.ProductViewSet)
router.register(r'employees', employee.EmployeeViewSet)
router.register(r'receipts', receipt.ReceiptViewSet)
router.register(r'helprequests', helprequest.HelpRequestViewSet)
router.register(r'imageuploads', imageupload.ImageUploadViewSet)
router.register(r'promotions', promotion.PromotionViewSet)
router.register(r'sections', section.SectionViewSet)
router.register(r'users', user.UserViewSet)
router.register(r'groups', user.GroupViewSet)
router.register(r'wishlists', wishlist.WishlistViewSet)
router.register(r'pulllists', pulllist.PulllistViewSet)
router.register(r'pulllistsubscriptions', pulllistsubscription.PulllistSubscriptionViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]