from datetime import timedelta
from django.utils.timezone import now
# Import the Post model from the current app's models.py
from .models import Post
# import Q for complex queries
from django.db.models import Q
from django.views.generic import ListView, DetailView

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
        return context

    ''' View to display the view of a single post'''
class PostDetailView(DetailView):
    model = Post
    template_name = 'artoon2d_blog/post_detail.html'
    context_object_name = 'post'