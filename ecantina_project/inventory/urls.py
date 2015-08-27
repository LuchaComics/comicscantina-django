from django.conf.urls import patterns, include, url
from inventory.views import print_label


urlpatterns = patterns('',
                       
    # Print Label
    #----------------------
    url(r'^inventory/(\d+)/(\d+)/print_label/comics$', print_label.print_label_comics_page),
)

