from django.db import models
from django.contrib.auth.models import User # Import the User model for the author field
from taggit.managers import TaggableManager # Import TaggableManager for tagging functionality
from django.contrib import admin

''' Model to rapresent a category for blog posts '''
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.name

''' Model to rapresent a user profile with follow functionality '''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    visitor_count = models.PositiveIntegerField(default=0)

    # New field with custom through model and unique related_name
    following = models.ManyToManyField(
        'self',
        through='Follow',
        symmetrical=False,
        related_name='new_followers',
        blank=True
    )

    def toggle_follow(self, target_profile):
        if Follow.objects.filter(from_profile=self, to_profile=target_profile).exists():
            Follow.objects.filter(from_profile=self, to_profile=target_profile).delete()
            return 'unfollowed'
        else:
            Follow.objects.create(from_profile=self, to_profile=target_profile)
            return 'followed'

    def __str__(self):
        return f"{self.user.username}'s profile"


class Follow(models.Model):
    from_profile = models.ForeignKey('Profile', related_name='following_relations', on_delete=models.CASCADE)
    to_profile = models.ForeignKey('Profile', related_name='follower_relations', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_profile', 'to_profile')

    def __str__(self):
        return f"{self.from_profile} follows {self.to_profile}"

''' Model to represent a blog post'''
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def toggle_like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
            return 'unliked'
        else:
            self.likes.add(user)
            return 'liked'

    def __str__(self):
        return f"{self.title} | {self.author}"

# Visitor Counter Model
class VisitorCounter(models.Model):
    total_visits = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Total visits: {self.total_visits}"