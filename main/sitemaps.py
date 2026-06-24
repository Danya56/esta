from django.contrib.sitemaps import Sitemap
from django.db.models.base import Model
from django.urls import reverse

class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return ['main_index', 'about_index', 'delivery_index']
    
    def priority(self, item):
        if item == "main_index":
            return 1.0
        return 0.5
    
    def location(self, obj: str): # type: ignore
        return reverse(obj)
    