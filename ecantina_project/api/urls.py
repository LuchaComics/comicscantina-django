from django.conf.urls import url, include
from api.views import api
from api.views import customer
from api.views import cart
from api.views import product
from api.views import employee
from rest_framework.urlpatterns import format_suffix_patterns

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    url(r'^api/$', api.api_root),
    url(r'^api/carts/$', cart.CartList.as_view(), name='cart-list'),
    url(r'^api/carts/(?P<pk>[0-9]+)/$', cart.CartDetail.as_view(), name='cart-detail'),
    url(r'^api/employees/$', employee.EmployeeList.as_view(), name='employee-list'),
    url(r'^api/employees/(?P<pk>[0-9]+)/$', employee.EmployeeDetail.as_view(), name='product-detail'),
    url(r'^api/products/$', product.ProductList.as_view(), name='product-list'),
    url(r'^api/products/(?P<pk>[0-9]+)/$', product.ProductDetail.as_view(), name='product-detail'),
    url(r'^api/customers/$', customer.CustomerList.as_view(), name='customer-list'),
    url(r'^api/customers/(?P<pk>[0-9]+)/$', customer.CustomerDetail.as_view(), name='customer-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns = format_suffix_patterns(urlpatterns)