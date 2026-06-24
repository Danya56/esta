from django.contrib import admin
from django.conf import settings
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import BlogSitemap
from main.sitemaps import StaticViewSitemap

sitemaps = {
    'blog': BlogSitemap,
    'static': StaticViewSitemap
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('', include('main.urls')),
    path('blog/', include('blog.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt', permanent=True)),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'icons/favicon.png', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
