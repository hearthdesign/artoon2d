from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from artoon2d_blog.sitemaps import PostSitemap, CategorySitemap, StaticViewSitemap
from django.views.generic import TemplateView

sitemaps = {
    'posts': PostSitemap,
    'categories': CategorySitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs (login/logout/password change, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Include all blog app URLs
    path('', include('artoon2d_blog.urls')),
]

# -------------------------------------------
# Robots & Sitemap (append to existing URLs)
# -------------------------------------------
urlpatterns += [    
    #Robot.txt
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="artoon2d_blog/robots.txt",
            content_type="text/plain",
        ),
    ),
    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
