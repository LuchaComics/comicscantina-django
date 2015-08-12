from django.conf.urls import patterns, include, url
from inventory_setting.views import org
from inventory_setting.views import stores
from inventory_setting.views import users
from inventory_setting.views import promo


urlpatterns = patterns('',
    # Org
    url(r'^inventory/(\d+)/(\d+)/settings/organization$', org.org_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/update_org_administrator$',org.ajax_update_org_administrator),
    # Store
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)$', stores.edit_store_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/save_logo$', stores.ajax_save_store_logo),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/save_data$', stores.ajax_save_store_data),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/section$', stores.ajax_section),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/delete_section$', stores.ajax_delete_section),
    url(r'^inventory/(\d+)/(\d+)/settings/store/(\d+)/refresh_sections$', stores.ajax_refresh_sections),
    url(r'^inventory/(\d+)/(\d+)/settings/store/new$', stores.store_settings_page),
    # Users
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)$', users.users_list_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)$', users.edit_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/new', users.add_user_settings_page),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_image$', users.ajax_save_employee_image),
    url(r'^inventory/(\d+)/(\d+)/settings/users/(\d+)/(\d+)/save_data$', users.ajax_save_user_data),
    url(r'^inventory/(\d+)/(\d+)/settings/users/delete/(\d+)$', users.ajax_delete_user),
    url(r'^inventory/(\d+)/(\d+)/settings/users/assign_employee$', users.ajax_assign_employee_to_store),
    # Promotions
    url(r'^inventory/(\d+)/(\d+)/settings/promotions$', promo.promo_settings_page),
)