from django.conf.urls import patterns, include, url
from inventory.views import customers
from inventory.views import comic_inventory_list
from inventory.views import print_label


urlpatterns = patterns('',
#                       # Custom Files
#                       url(r'^robots\.txt$', txt.robots_txt_page),
#                       url(r'^humans\.txt$', txt.humans_txt_page),
#
                                                           
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