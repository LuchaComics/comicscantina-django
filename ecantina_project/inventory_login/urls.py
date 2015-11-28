from django.conf.urls import patterns, include, url
from . import views

urlpatterns = patterns('',
    # Logging In / Logging Out
    url(r'^inventory/login$', views.login_page, name='login'),
)

