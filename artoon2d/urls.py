from django.contrib import admin
from django.urls import path, include
from artoon2d_blog import views
from artoon2d_blog.views import PostListView

# Import static to serve media files
from django.conf.urls.static import static
# Import settings to serve media files
from django.conf import settings


urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    # Autentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    # include the blog APP' s URLs
    path('', include('artoon2d_blog.urls')),
    # Direct access to the postlist view
    path('posts/', PostListView.as_view(), name='post_list'),
    # User profile view
    path('profile/<int:user_id>/', views.user_profile, name='user_profile'),
]

# Serve media files during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
