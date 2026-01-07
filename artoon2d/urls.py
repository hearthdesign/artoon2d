from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication URLs (login/logout/password change, etc.)
    path('accounts/', include('django.contrib.auth.urls')),

    # Include all blog app URLs
    path('', include('artoon2d_blog.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
