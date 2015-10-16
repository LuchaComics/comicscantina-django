from django.conf.urls import patterns, include, url
from register.views import inventory
from register.views import store

urlpatterns = patterns('',
    # Inventory
    url(r'^inventory/register$', inventory.store_registration_page, name='register'),
    url(r'^inventory/save_image$', inventory.ajax_store_save_image),
    url(r'^inventory/create_account$', inventory.ajax_create_account),
    url(r'^inventory/registered_successful$', inventory.store_registation_successful_page, name='registered_successful'),
                       
    # Store
    url(r'^store/register/step1$', store.registration_step1_page, name='store_register'),
    url(r'^store/register/step2$', store.registration_step2_page),
    url(r'^store/register/step3$', store.registration_step3_page),
)

