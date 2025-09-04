from datetime import timedelta
from django.utils.timezone import now
# Import the Post model from the current app's models.py
from .models import Post
from django.shortcuts import render
# import Q for complex queries
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Import mixins for authentication and authorization
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

## Import user creation form for user registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
# Import get object or 404 and redirect for like and follow views
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


'''View to display a list of blog posts with search and sorting functionality'''
class PostListView(ListView):
    model = Post
    template_name = 'artoon2d_blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5
    # Override get queryset to add search and filtering function
    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category')
        recent_days = self.request.GET.get('recent_days')
        qs = Post.objects.all()
        # Filter by recent days if defined and valid
        if recent_days:
            try:
                days = int(recent_days)
                cutoff = now() - timedelta(days=days)
                qs = qs.filter(created_at__gte=cutoff)
            except ValueError:
                pass  # ignore invalid input
        # Filter by search query in title, content or tags
        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        # filter by category if defined
        if category:
            qs = qs.filter(category__name__iexact=category)
        # order by most recent posts first
        return qs.order_by('-created_at')
    # Add context data for template rendering
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        context['category'] = self.request.GET.get('category')
        context['recent_days'] = self.request.GET.get('recent_days')
        context['recent_posts'] = Post.objects.order_by('-created_at')[:5]
        return context

''' View to display the view of a single post'''
class PostDetailView(DetailView):
    model = Post
    template_name = 'artoon2d_blog/post_detail.html'
    context_object_name = 'post'

''' Import to create a new blog post '''
from django.views.generic.edit import CreateView
from .models import Post

''' View to create a new blog post '''
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'author', 'image' 'category', 'tags', 'theme',]
    template_name = 'artoon2d_blog/post_form.html' # Template for the form
    success_url = reverse_lazy('post_list') # Redirect to Home after seccessful creation
    # Automatically set the author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

''' View to update an existing blog post'''
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tags']
    template_name = 'artoon2d_blog/post_form.html'
    success_url = reverse_lazy('post_list')
    # Ensure that only the author can edit the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

''' View to delete a blog post '''
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'artoon2d_blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
    # Ensure only the author can delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
''' Home view to render the home page '''    
def home(request):
    return render(request, 'artoon2d_blog/home.html')

# View to handle user registration
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

''' View to handle user account deletion'''
class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User  # Use the User model
    template_name = 'registration/account_confirm_delete.html'
    success_url = reverse_lazy('home')  # Redirect after deletion
    # Ensure only the logged-in user can delete their own account
    def get_object(self):
        return self.request.user  # Only allow users to delete themselves

''' View to like or unlike a post '''
@login_required(login_url='register')
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    action = post.toggle_like(request.user)
    # Optional: Add messages or logging here
    return redirect('post_detail', pk=post_id)

''' View to follow or unfollow a user '''
@login_required(login_url='register')
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = request.user.profile
    action = profile.toggle_follow(target_user)
    # Optional: Add messages or logging here
    return redirect('user_profile', user_id=target_user.id)