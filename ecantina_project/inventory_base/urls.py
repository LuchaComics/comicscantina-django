from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', views.robots_txt_page),
    url(r'^humans\.txt$', views.humans_txt_page)
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)