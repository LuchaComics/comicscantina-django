from django.conf.urls import patterns, include, url
from . import views


urlpatterns = patterns('',
    # Custom Files
    url(r'^robots\.txt$', views.robots_txt_page, name='robots'),
    url(r'^humans\.txt$', views.humans_txt_page, name='humans'),
    url(r'^F860DA3DF4C3F8A7F5EAFFDA1DB33807\.txt$', views.comodo_txt_page, name='comodo'),
)

# Captchas
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)