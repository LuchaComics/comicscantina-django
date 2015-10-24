from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from api.models.ec.organization import Organization
from api.models.ec.store import Store
from api.models.ec.product import Product


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['store_landpage', 'store_products', 'robots', 'humans', 'store_register', 'store_tos', 'store_privacy',]
    
    def location(self, item):
        return reverse(item)


class OrganizationSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return Organization.objects.filter(is_suspended=False)
    
    def lastmod(self, obj):
        return obj.last_updated


class StoreSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return Store.objects.filter(is_suspended=False)
    
    def lastmod(self, obj):
        return obj.last_updated


class ProductsSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'
    
    def items(self):
        return Product.objects.filter(is_sold=False)
    
    def lastmod(self, obj):
        return obj.last_updated

# https://docs.djangoproject.com/en/1.8/ref/contrib/sitemaps/