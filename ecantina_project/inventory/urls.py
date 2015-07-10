from django.conf.urls import patterns, include, url
from inventory.views import dashboard
from inventory.views import list
from inventory.views import setting_org
from inventory.views import setting_stores
from inventory.views import setting_users
from inventory.views import help
from inventory.views import customers
from inventory.views import checkout
from inventory.views import comics_searching
from inventory.views import comics_add

urlpatterns = patterns('',
#                       # Custom Files
#                       url(r'^robots\.txt$', txt.robots_txt_page),
#                       url(r'^humans\.txt$', txt.humans_txt_page),
#
                       
    # Dashboard
    #------------
    url(r'^inventory/(\d+)/(\d+)$', dashboard.dashboard_page),
    url(r'^inventory/(\d+)/(\d+)/dashboard$', dashboard.dashboard_page),
                       
    # Settings
    #-------------
    # Org
    url(r'^inventory/(\d+)/(\d+)/settings/organization$', setting_org.org_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/save_org_logo$', setting_org.ajax_org_save_logo),
    url(r'^inventory/(\d+)/(\d+)/settings/save_org_data$', setting_org.ajax_save_org_data),
    # Store
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)$', setting_stores.edit_store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/save_logo$', setting_stores.ajax_save_store_logo),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/save_data$', setting_stores.ajax_save_store_data),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/section$', setting_stores.ajax_section),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/delete_section$', setting_stores.ajax_delete_section),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/refresh_sections$', setting_stores.ajax_refresh_sections),
    url(r'^inventory/(\d+)/(\d+)/settings/store/new$', setting_stores.store_settings_page),
    # Users
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)$', setting_users.users_list_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)$', setting_users.edit_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/new', setting_users.add_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_image$', setting_users.ajax_save_employee_image),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_data$', setting_users.ajax_save_user_data),
    url(r'^inventory/(\d+)/(\d+)/settings/users/delete/(\d+)$', setting_users.ajax_delete_user),
    url(r'^inventory/(\d+)/(\d+)/settings/users/assign_employee$', setting_users.ajax_assign_employee_to_store),
             
    # Help
    #-------------
    url(r'^inventory/(\d+)/(\d+)/help$', help.help_page),
    url(r'^inventory/(\d+)/(\d+)/help/save_image$', help.ajax_save_image),
    url(r'^inventory/(\d+)/(\d+)/help/save_data$', help.ajax_save_data),
               
    # Customers
    #-------------
    url(r'^inventory/(\d+)/(\d+)/customers$', customers.customers_page),
    url(r'^inventory/(\d+)/(\d+)/customers/refresh_table$', customers.ajax_refresh_table),
    url(r'^inventory/(\d+)/(\d+)/customers/delete$', customers.ajax_delete_customer),
    url(r'^inventory/(\d+)/(\d+)/add_customer$', customers.add_customer_page),
    url(r'^inventory/(\d+)/(\d+)/add_customer/submit$', customers.ajax_add_customer),
                       
    # Checkout
    #-------------
    url(r'^inventory/(\d+)/(\d+)/checkout$', checkout.checkout_page),
                       
                       
    # Add Inventory Item
    #-------------
    # Comics
    url(r'^inventory/(\d+)/(\d+)/add/comic$', comics_searching.search_comics_page),
    url(r'^inventory/(\d+)/(\d+)/add/search_comics$', comics_searching.ajax_search_comics),
    url(r'^inventory/(\d+)/(\d+)/add/(\d+)$', comics_add.add_product_page),
    url(r'^inventory/add/(\d+)/section_dropbox/(\d+)$', comics_add.sections_per_location),
    url(r'^inventory/add/(\d+)/upload_cover$', comics_add.save_uploaded_cover),
    url(r'^inventory/add/(\d+)/add_product$', comics_add.add_product),
    url(r'^inventory/add/(\d+)/list_products$', comics_add.list_products),
                      
                       
                       
                       
                       
    # TODO: Update all entries below.
    #---------------------------------------------------------------------------
                       
    # Inventory List
#    url(r'^inventory/list$', list.list_page),
#                       
#    
#    
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)