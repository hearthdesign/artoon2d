from django.contrib import admin
from django.urls import path, include
from artoon2d_blog.views import PostListView

# Import static to serve media files
from django.conf.urls.static import static
# Import settings to serve media files
from django.conf import settings 


urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    # include the blog app' s URLs
    path('', include('artoon2d_blog.urls')),
    # Direct access to the postlist view
    path('posts/', PostListView.as_view(), name='post_list'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)