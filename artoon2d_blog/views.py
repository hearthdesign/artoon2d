from datetime import timedelta
from django.utils.timezone import now
# Import the Post model from the current app's models.py
from .models import Post
from django.shortcuts import render
# import Q for complex queries
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
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

''' View to create a new blog post'''
from django.views.generic.edit import CreateView
from .models import Post

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'author', 'image' 'category', 'tags', 'theme',] 
    template_name = 'artoon2d_blog/post_form.html' # Template for the form
    success_url = '/' # Redirect to Home afret seccessful creation

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tags']
    template_name = 'artoon2d_blog/post_form.html' # Template for the form
    success_url = reverse_lazy('post_list') # Redirect to Home afret seccessful creation
    # Automatically set the author to the logged-in user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tags']
    template_name = 'artoon2d_blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'artoon2d_blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
def home(request):
    return render(request, 'artoon2d_blog/home.html')

# View to handle user registration
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')  