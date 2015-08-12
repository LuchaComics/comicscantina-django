from django.conf.urls import url, include
from api.views import comic
from api.views import customer
from api.views import organization
from api.views import store
from api.views import product
from api.views import employee
from api.views import receipt
from api.views import helprequest
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'comics', comic.ComicViewSet)
router.register(r'organization', organization.OrganizationViewSet)
router.register(r'customers', customer.CustomerViewSet)
router.register(r'stores', store.StoreViewSet)
router.register(r'products', product.ProductViewSet)
router.register(r'employees', employee.EmployeeViewSet)
router.register(r'receipts', receipt.ReceiptViewSet)
router.register(r'helprequests', helprequest.HelpRequestViewSet)


# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]