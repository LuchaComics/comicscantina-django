from django.conf.urls import patterns, include, url
from inventory_setting.views import admin
from inventory_setting.views import org
from inventory_setting.views import stores
from inventory_setting.views import employees
from inventory_setting.views import promo
from inventory_setting.views import tag


urlpatterns = patterns('',
                       
    # Admin
    url(r'^inventory/(\d+)/(\d+)/settings/administrator$', admin.admin_settings_page),
    url(r'^user/settings/update_password$',admin.ajax_update_password),
    # Org
    url(r'^inventory/(\d+)/(\d+)/settings/organization$', org.org_settings_page),
    # Store
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)$', stores.edit_store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/store/new$', stores.store_settings_page),
    # Employee
    url(r'^inventory/(\d+)/(\d+)/settings/employee/(\d+)$', employees.users_list_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/employee/new', employees.add_employee_page),
    url(r'^inventory/(\d+)/(\d+)/settings/employee/edit/(\d+)$', employees.edit_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/assign_employee$', employees.ajax_assign_employee_to_store),
    # Promotions
    url(r'^inventory/(\d+)/(\d+)/settings/promotions$', promo.promo_settings_page),
    # Tags
    url(r'^inventory/(\d+)/(\d+)/settings/tags$', tag.tags_settings_page),
)