from django.conf.urls import patterns, include, url
from inventory.views import setting_org
from inventory.views import setting_stores
from inventory.views import setting_users
from inventory.views import customers
from inventory.views import comic_inventory_list
from inventory.views import print_label


urlpatterns = patterns('',
#                       # Custom Files
#                       url(r'^robots\.txt$', txt.robots_txt_page),
#                       url(r'^humans\.txt$', txt.humans_txt_page),
#
                                              
    # Settings
    #----------------------
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
             
    # Customers
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/customers$', customers.customers_page),
    url(r'^inventory/(\d+)/(\d+)/customers/refresh_table$', customers.ajax_refresh_table),
    url(r'^inventory/(\d+)/(\d+)/customers/delete$', customers.ajax_delete_customer),
    url(r'^inventory/(\d+)/(\d+)/add_customer$', customers.add_customer_page),
    url(r'^inventory/(\d+)/(\d+)/add_customer/submit$', customers.ajax_add_customer),
                       
    # Inventory List
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/list/comics$', comic_inventory_list.list_comics_page),
    url(r'^inventory/(\d+)/(\d+)/list/search_comics$', comic_inventory_list.ajax_search_comics),
                       
    # Print Label
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/print_label/comics$', print_label.print_label_comics_page),
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)