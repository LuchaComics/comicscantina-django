from django.conf.urls import patterns, include, url
from login.views import inventory
from login.views import store

urlpatterns = patterns('',
    # Logging In / Logging Out
    url(r'^inventory/login$', inventory.login_page, name='login'),
    url(r'^inventory/login_authentication$', inventory.ajax_login_authentication),
    url(r'^inventory/logout_authentication$', inventory.ajax_logout_authentication),
    url(r'^store/login_authentication$', store.ajax_login_authentication),
    url(r'^store/logout_authentication$', store.ajax_logout_authentication),
)

