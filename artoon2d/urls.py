from django.contrib import admin
from django.urls import path, include
from artoon2d_blog.views import PostListView

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),
    # include the blog app' s URLs
    path('', include('artoon2d_blog.urls')),
    # Add a URL pattern for the postlist view
    path('posts/', PostListView.as_view(), name='post_list'),
]