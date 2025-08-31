from django.shortcuts import render
# Import Django's generic class-based views for listing and detail display
from django.views.generic import ListView, DetailView
# Import the Post model from the current app's models.py
from .models import Post

# View to display a list of blog posts
class PostListView(ListView):
    # Specify the model this view will operate on
    model = Post
    # Define the template to render the list of posts
    template_name = 'blog/post_list.html'
    # In the template, use {{ posts }} to access the list
    context_object_name = 'posts'

# View to display a single blog post
class PostDetailView(DetailView):
    # Specify the model this view will operate on
    model = Post
    # Define the template to render the detailed view of a single post
    template_name = 'blog/post_detail.html'