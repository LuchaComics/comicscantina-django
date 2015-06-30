from django.conf.urls import patterns, include, url
from inventory.views import dashboard
from inventory.views import list
from inventory.views import add
from inventory.views import add_comic
from inventory.views import search
from inventory.views import setting

urlpatterns = patterns('',
#                       # Custom Files
#                       url(r'^robots\.txt$', txt.robots_txt_page),
#                       url(r'^humans\.txt$', txt.humans_txt_page),
#
                       
    # Dashboard
    url(r'^inventory/(\d+)/(\d+)$', dashboard.dashboard_page),
    url(r'^inventory/(\d+)/(\d+)/dashboard$', dashboard.dashboard_page),
                       
    # Settings
    url(r'^inventory/(\d+)/(\d+)/settings/organization$', setting.org_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/save_org_logo$', setting.ajax_org_save_logo),
    url(r'^inventory/(\d+)/(\d+)/settings/save_org_data$', setting.ajax_save_org_data),
    url(r'^inventory/(\d+)/(\d+)/settings/stores$', setting.store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/locations$', setting.store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users$', setting.store_settings_page),
             
    # Inventory Adding
    url(r'^inventory/(\d+)/(\d+)/add/comic$', add_comic.search_page),
    url(r'^inventory/(\d+)/(\d+)/search_comics$', add_comic.ajax_search),
                       
                       
    # TODO: Update all entries below.
    #---------------------------------------------------------------------------
    # Inventory List
    url(r'^inventory/list$', list.list_page),
                       
    
    url(r'^inventory/add/(\d+)$', add.add_product_page),
    url(r'^inventory/add/(\d+)/section_dropbox/(\d+)$', add.sections_per_location),
    url(r'^inventory/add/(\d+)/upload_cover$', add.save_uploaded_cover),
    url(r'^inventory/add/(\d+)/add_product$', add.add_product),
    url(r'^inventory/add/(\d+)/list_products$', add.list_products),
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)