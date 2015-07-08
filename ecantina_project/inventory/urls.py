from django.conf.urls import patterns, include, url
from inventory.views import dashboard
from inventory.views import list
from inventory.views import add
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
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)$', setting.edit_store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/save_logo$', setting.ajax_save_store_logo),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/save_data$', setting.ajax_save_store_data),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/section$', setting.ajax_section),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/delete_section$', setting.ajax_delete_section),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/refresh_sections$', setting.ajax_refresh_sections),
    url(r'^inventory/(\d+)/(\d+)/settings/store/new$', setting.store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)$', setting.users_list_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)$', setting.edit_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/new', setting.add_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_image$', setting.ajax_save_employee_image),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_data$', setting.ajax_save_user_data),
    url(r'^inventory/(\d+)/(\d+)/settings/users/delete/(\d+)$', setting.ajax_delete_user),
             
    # Inventory Searching/Adding
    url(r'^inventory/(\d+)/(\d+)/add/comic$', search.search_comics_page),
    url(r'^inventory/(\d+)/(\d+)/add/search_comics$', search.ajax_search_comics),
    url(r'^inventory/(\d+)/(\d+)/add/(\d+)$', add.add_product_page),
                       
                       
    # TODO: Update all entries below.
    #---------------------------------------------------------------------------
    # Inventory List
    url(r'^inventory/list$', list.list_page),
                       
    
    
    url(r'^inventory/add/(\d+)/section_dropbox/(\d+)$', add.sections_per_location),
    url(r'^inventory/add/(\d+)/upload_cover$', add.save_uploaded_cover),
    url(r'^inventory/add/(\d+)/add_product$', add.add_product),
    url(r'^inventory/add/(\d+)/list_products$', add.list_products),
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)