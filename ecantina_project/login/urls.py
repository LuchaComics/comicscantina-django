from django.conf.urls import patterns, include, url
from login.views import inventory

urlpatterns = patterns('',
    # Logging In / Logging Out
    url(r'^inventory/login$', inventory.login_page, name='login'),
    url(r'^inventory/login_authentication$', inventory.login_authentication),
    url(r'^inventory/logout_authentication$', inventory.logout_authentication),
)

