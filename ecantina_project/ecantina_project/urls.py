"""ecantina_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static, settings
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('inventory.urls')),
#    url(r'', include('store_base.urls')), # uncomment if plan on using.
    url(r'', include('store_landpage.urls')),
    url(r'', include('store_about.urls')),
    url(r'', include('store_products.urls')),
    url(r'', include('store_blog.urls')),
    url(r'', include('store_checkout.urls')),
    url(r'', include('store_customer.urls')),               
    url(r'', include('register.urls')),
    url(r'', include('login.urls')),
#    url(r'', include('inventory_base.urls')) # uncomment if plan on using.
    url(r'', include('inventory_add_product.urls')),
    url(r'', include('inventory_checkout.urls')),
    url(r'', include('inventory_order.urls')),
    url(r'', include('inventory_customer.urls')),
    url(r'', include('inventory_dashboard.urls')),
    url(r'', include('inventory_help.urls')),
    url(r'', include('inventory_print_label.urls')),
    url(r'', include('inventory_products.urls')),
    url(r'', include('inventory_setting.urls')),
    url(r'', include('inventory_email.urls')),
    url(r'', include('api.urls')),
               
    # Sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
               
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
