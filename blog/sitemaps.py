from django.contrib.sitemaps import Sitemap
from .models import Article

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Article.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at