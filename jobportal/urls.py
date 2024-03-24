from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from modules.job.sitemaps import StaticSitemap, ArticleSitemap
from modules.job.feeds import LatestArticlesFeed

sitemaps = {
    'static': StaticSitemap,
    'articles': ArticleSitemap
}

urlpatterns = [
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('admin/', admin.site.urls),
    path('feeds/latest/', LatestArticlesFeed(), name='latest_articles_feed'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('modules.job.urls')),
    path('', include('modules.system.urls')),
]

if settings.DEBUG:
    urlpatterns = [path('__debug__/', include('debug_toolbar.urls'))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
