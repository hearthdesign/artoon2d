from datetime import timedelta
from django.utils.timezone import now
# Import the Post model from the current app's models.py
from .models import Post, Profile

# import Q for complex queries
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
# Import mixins for authentication and authorization
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
''' Import to create a new blog post '''
from django.views.generic.edit import CreateView

from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST

## Import user creation form for user registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Import get object or 404 and redirect for like and follow views
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from artoon2d_blog.models import Follow

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
        # "is_following" flag for each post's author
        user = self.request.user
        if user.is_authenticated:
            profile, _ = Profile.objects.get_or_create(user=user)
            for post in context['posts']:
                author_profile, _ = Profile.objects.get_or_create(user=post.author)
                post.author.is_following = profile.following.filter(id=post.author.id).exists()
                post.author.follower_count = Follow.objects.filter(to_profile=author_profile).count()
        return context

''' View to display the view of a single post'''
class PostDetailView(DetailView):
    model = Post
    template_name = 'artoon2d_blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context['post']
        user = self.request.user

        if user.is_authenticated and user != post.author:
            profile, _ = Profile.objects.get_or_create(user=user)
            post.author.is_following = profile.following.filter(id=post.author.id).exists()
            post.author.follower_count = post.author.profile.new_followers.count()

        return context

''' View to create a new blog post '''
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tags', 'theme']
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
    # Limit to latest 10 posts with images for the main section
    posts_with_images = Post.objects.exclude(image='').order_by('-created_at')[:10]

    # Add recent posts for the sidebar (e.g., latest 5 posts)
    recent_posts = Post.objects.order_by('-created_at')[:5]

    return render(request, 'artoon2d_blog/home.html', {
        'posts': posts_with_images,
        'recent_posts': recent_posts
    })


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

@require_POST

def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    action = post.toggle_like(request.user)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({"status": action, "likes": post.likes.count()})
    return redirect('post_detail', pk=post_id)

def about_view(request):
    return render(request, 'artoon2d_blog/about.html')

''' View to follow or unfollow a user '''
@login_required(login_url='register')
@require_POST
def follow_user(request, user_id):
    # Get the target profile based on user ID
    target_profile = get_object_or_404(Profile, user__id=user_id)
    user_profile = request.user.profile

    # Toggle follow status
    action = user_profile.toggle_follow(target_profile)

    # Handle AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        follower_count = target_profile.follower_relations.count()
        return JsonResponse({
            "status": action,
            "follower_count": follower_count
        })

    # Handle non-AJAX request with feedback
    messages.success(
        request,
        f"You {action} {target_profile.user.username}."
    )
    return redirect('user_profile', user_id=target_profile.user.id)

def user_profile(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile, _ = Profile.objects.get_or_create(user=target_user)

    # Visitor count logic
    if request.user.is_authenticated and request.user != target_user:
        profile.visitor_count = profile.visitor_count + 1 if profile.visitor_count else 1
        profile.save()

    # Posts by this user
    posts = target_user.post_set.all()

    context = {
        'user_profile': target_user,
        'profile': profile,
        'posts': posts,
        'is_following': request.user.is_authenticated and profile.followers.filter(id=request.user.id).exists(),
        'follower_count': profile.followers.count(),
        'visitor_count': profile.visitor_count or 0,
    }
    return render(request, 'artoon2d_blog/user_profile.html', context)
