# artoon2d_blog/urls.py
from django.urls import path
# Import settings to serve media files
from django.conf import settings
from . import views
# Import views from the current app
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, AccountDeleteView

# Import static to serve media files
from django.conf.urls.static import static
# Import like and follow views
from .views import like_post, follow_user

from .views import (
    home,
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

from .views import RegisterView

# Define URL patterns for the blog app
urlpatterns = [
    path('', views.home, name='home'),
    # URL pattern for the list of posts
    path('', PostListView.as_view(), name='post-list'),


    # URL pattern for creating a new post
    path('post/new/', PostCreateView.as_view(),
         name='post_create'),  # List of posts
    path('posts/new/', PostCreateView.as_view(),
         name='post_create_alt'),  # Create post
    # URL patterns for updating an existing post identified by the primary key
    path('post/<int:pk>/', PostDetailView.as_view(),
         name='post_detail'),  # View post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(),
         name='post_update'),  # Edit post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(),
         name='post_delete'),  # Delete post
    path('accounts/register/', RegisterView.as_view(),
         name='register'),  # Register
    path('accounts/delete/', AccountDeleteView.as_view(),
         name='account_delete'),  # Delete account
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('about/', views.about_view, name='about')
]
