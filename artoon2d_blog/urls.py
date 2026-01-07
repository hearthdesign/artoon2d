# artoon2d_blog/urls.py
from django.urls import path
# Import settings to serve media files
from django.conf import settings
# Import static to serve media files
from django.conf.urls.static import static
# Import authentication view
from django.contrib.auth.views import LoginView, LogoutView
# Import views from the current app
from .views import (
     home, 
     PostListView, 
     PostDetailView, 
     PostCreateView, 
     PostUpdateView, 
     PostDeleteView, 
     RegisterView, 
     AccountDeleteView, 
     user_profile,
     like_post, 
     follow_user, 
     about_view,
     user_profile,
     )
    

# Define URL patterns for the blog app
urlpatterns = [ 
     path('', home, name='home'),
     # Post 
     path('posts/', PostListView.as_view(), name='post_list'),
     path('post/new/', PostCreateView.as_view(), name='post_create'),
     path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'), # SEO friendly
     path('post/id/<int:pk>/', PostDetailView.as_view(), name='post_detail_by_id'), # fallback numeric ID
     path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
     path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

     # Category posts
     path('category/<slug:slug>/', PostListView.as_view(), name='category_posts'),

     # User profile
     path('user/<int:user_id>/', user_profile, name='user_profile'),

     # Auth
     path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'), 
     path('accounts/logout/', LogoutView.as_view(), name='logout'),
     path('accounts/register/', RegisterView.as_view(), name='register'), 
     path('accounts/delete/', AccountDeleteView.as_view(), name='account_delete'),

     # Actions: Likes & follows
     path('like/<int:post_id>/', like_post, name='like_post'), 
     path('follow/<int:user_id>/', follow_user, name='follow_user'),

     # Static pages 
     path('about/', about_view, name='about'),
]

     # Media files (local dev only) 
if settings.DEBUG: 
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

