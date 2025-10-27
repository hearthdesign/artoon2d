from django.db import models
from django.contrib.auth.models import User # Import the User model for the author field
from taggit.managers import TaggableManager # Import TaggableManager for tagging functionality
from django.contrib import admin
from django.contrib.auth.models import User

''' Model to rapresent a blog post'''
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey('artoon2d_blog.Category', on_delete=models.SET_NULL, null=True, blank=True)
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


    
''' Model to rapresent a category for blog posts '''
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

''' Model to rapresent a user profile with following functionality '''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(User, related_name='followers', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    visitor_count = models.PositiveIntegerField(default=0)

    # toggle follow method to follow or unfollow a user
    def toggle_follow(self, target_user):
        if target_user in self.following.all():
            self.following.remove(target_user)
            target_user.profile.followers.remove(self.user)
            return 'unfollowed'
        else:
            self.following.add(target_user)
            target_user.profile.followers.add(self.user)
            return 'followed'