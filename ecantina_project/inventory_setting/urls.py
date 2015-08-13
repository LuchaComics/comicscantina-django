from django.conf.urls import patterns, include, url
from inventory_setting.views import org
from inventory_setting.views import stores
from inventory_setting.views import employees
from inventory_setting.views import promo


urlpatterns = patterns('',
    # Org
    url(r'^inventory/(\d+)/(\d+)/settings/organization$', org.org_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/update_org_administrator$',org.ajax_update_org_administrator),
    # Store
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)$', stores.edit_store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/store/new$', stores.store_settings_page),
    # Users
    url(r'^inventory/(\d+)/(\d+)/settings/employee/(\d+)$', employees.users_list_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/employee/new', employees.add_employee_page),
    url(r'^inventory/(\d+)/(\d+)/settings/employee/edit/(\d+)$', employees.edit_user_settings_page),
    
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_image$', employees.ajax_save_employee_image),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_data$', employees.ajax_save_user_data),
    url(r'^inventory/(\d+)/(\d+)/settings/users/delete/(\d+)$', employees.ajax_delete_user),
    url(r'^inventory/(\d+)/(\d+)/settings/users/assign_employee$', employees.ajax_assign_employee_to_store),
    # Promotions
    url(r'^inventory/(\d+)/(\d+)/settings/promotions$', promo.promo_settings_page),
)