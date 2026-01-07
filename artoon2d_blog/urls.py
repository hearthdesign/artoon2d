# artoon2d_blog/urls.py
from django.urls import path
# Import settings to serve media files
from django.conf import settings
# Import static to serve media files
from django.conf.urls.static import static

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
     like_post, 
     follow_user, 
     about_view, 
     )
    

# Define URL patterns for the blog app
urlpatterns = [ 
     path('', home, name='home'),
     # Post list 
     path('posts/', PostListView.as_view(), name='post_list'),

     # Post CRUD
     path('post/new/', PostCreateView.as_view(), name='post_create'),
     path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
     path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
     path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),

     # Auth
     path('accounts/register/', RegisterView.as_view(), name='register'), 
     path('accounts/delete/', AccountDeleteView.as_view(), name='account_delete'),

     # Likes & follows
     path('like/<int:post_id>/', like_post, name='like_post'), 
     path('follow/<int:user_id>/', follow_user, name='follow_user'),

     # Static pages 
     path('about/', about_view, name='about'), 
]

     # Media files (local dev only) 
if settings.DEBUG: 
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

