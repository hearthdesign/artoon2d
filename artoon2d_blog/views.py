from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Q, Count, Exists, OuterRef, F
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.decorators.http import require_POST
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Profile, Category, VisitorCounter
from .models import Follow

# ---------------------------------------------------------------------
# Tobots.txt
# ---------------------------------------------------------------------
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Sitemap: " + request.build_absolute_uri("/sitemap.xml"),
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# ---------------------------------------------------------------------
# Post List
# ---------------------------------------------------------------------
@method_decorator(cache_page(60 * 5), name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'artoon2d_blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        qs = (
            Post.objects
            .select_related('author', 'author__profile', 'category')
            .prefetch_related('tags')
            .annotate(
                follower_count=Count(
                    'author__profile__follower_relations',
                    distinct=True
                )
            )
        )

        user = self.request.user
        if user.is_authenticated:
            qs = qs.annotate(
                is_following=Exists(
                    Follow.objects.filter(
                        from_profile__user=user,
                        to_profile__user=OuterRef('author')
                    )
                )
            )

        query = self.request.GET.get('q')
        category_slug = self.kwargs.get('slug') or self.request.GET.get('category')
        recent_days = self.request.GET.get('recent_days')

        if recent_days and recent_days.isdigit():
            qs = qs.filter(
                created_at__gte=now() - timedelta(days=int(recent_days))
            )

        if query:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()

        if category_slug:
            qs = qs.filter(category__slug=category_slug)

        return qs.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'recent_posts': Post.objects.order_by('-created_at')[:5],
            'query': self.request.GET.get('q'),
            'category': self.request.GET.get('category'),
            'recent_days': self.request.GET.get('recent_days'),
        })
        return context


# ---------------------------------------------------------------------
# Post Detail
# ---------------------------------------------------------------------
class PostDetailView(DetailView):
    model = Post
    template_name = 'artoon2d_blog/post_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related('author', 'author__profile', 'category')
            .prefetch_related('tags')
            .annotate(
                follower_count=Count(
                    'author__profile__follower_relations',
                    distinct=True
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['canonical_url'] = self.request.build_absolute_uri(
            self.object.get_absolute_url()
        )
        post = context['post']
        user = self.request.user

        context['is_following'] = (
            user.is_authenticated and
            Follow.objects.filter(
                from_profile__user=user,
                to_profile = getattr(post.author, "profile", None)
            ).exists()
        )

        return context


# ---------------------------------------------------------------------
# Create / Update / Delete Post
# ---------------------------------------------------------------------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tags', 'theme']
    template_name = 'artoon2d_blog/post_form.html'
    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'category', 'tags', 'theme']
    template_name = 'artoon2d_blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user == self.get_object().author


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'artoon2d_blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        return self.request.user == self.get_object().author
    
    # Clear cache after post deletion
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        cache.clear()   
        return response

# ---------------------------------------------------------------------
# Home
# ---------------------------------------------------------------------
@cache_page(60 * 5)  # 5 minutes
def home(request):
    counter, created = VisitorCounter.objects.get_or_create(
        id=1,
        defaults={'total_visits': 1}
    )

    if not created:
        VisitorCounter.objects.filter(id=counter.id).update(
            total_visits=F('total_visits') + 1
        )
        counter.refresh_from_db()

    posts = (
        Post.objects
        .filter(image__isnull=False)
        .exclude(image='')
        .select_related('author')
        .order_by('-created_at')[:10]
    )

    recent_posts = Post.objects.order_by('-created_at')[:5]

    return render(request, 'artoon2d_blog/home.html', {
        'posts': posts,
        'recent_posts': recent_posts,
        'visitor_count': counter.total_visits,
    })

# ---------------------------------------------------------------------
# Registration & Account
# ---------------------------------------------------------------------
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'registration/account_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

# ---------------------------------------------------------------------
# Likes
# ---------------------------------------------------------------------
@login_required(login_url='register')
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    action = post.toggle_like(request.user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': action,
            'likes': post.likes.count()
        })

    return redirect('post_detail', slug=post.slug)


# ---------------------------------------------------------------------
# Follow / Unfollow
# ---------------------------------------------------------------------
@login_required(login_url='register')
@require_POST
def follow_user(request, user_id):
    target_profile = get_object_or_404(Profile, user__id=user_id)
    user_profile = request.user.profile

    action = user_profile.toggle_follow(target_profile)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'status': action,
            'follower_count': target_profile.follower_relations.count()
        })

    messages.success(
        request,
        f"You {action} {target_profile.user.username}."
    )
    return redirect('user_profile', user_id=user_id)


# ---------------------------------------------------------------------
# User Profile
# ---------------------------------------------------------------------
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile

    if request.user.is_authenticated and request.user != user:
        Profile.objects.filter(pk=profile.pk).update(
            visitor_count=F('visitor_count') + 1
        )
        profile.refresh_from_db(fields=['visitor_count'])

    posts = (
        Post.objects
        .filter(author=user)
        .select_related('category')
        .order_by('-created_at')
    )

    is_following = (
        request.user.is_authenticated and
        Follow.objects.filter(
            from_profile__user=request.user,
            to_profile=profile
        ).exists()
    )

    return render(request, 'artoon2d_blog/user_profile.html', {
        'user_profile': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
        'follower_count': profile.follower_relations.count(),
        'visitor_count': profile.visitor_count or 0,
    })


# ---------------------------------------------------------------------
# Static Pages
# ---------------------------------------------------------------------
def about_view(request):
    return render(request, 'artoon2d_blog/about.html')
