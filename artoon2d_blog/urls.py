# artoon2d_blog/urls.py
from django.urls import path
# Import views from the current app
from .views import PostListView, PostDetailView

# Define URL patterns for the blog app
urlpatterns = [
    # URL pattern for the list of posts
    path('', PostListView.as_view(), name='post-list'),
    # URL pattern for  the view of a single post identified by the primary key
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
