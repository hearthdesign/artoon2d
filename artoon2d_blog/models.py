from django.db import models
from django.contrib.auth.models import User # Import the User model for the author field
from taggit.managers import TaggableManager # Import TaggableManager for tagging functionality

''' Model to rapresent a blog post'''
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    theme = models.CharField (max_length=100, blank=True, null=True)
    # on delete= SET_NULL to avoid deleting posts if a category is deleted
    category = models.ForeignKey('artoon2d_blog.Category', on_delete=models.SET_NULL, null=True, blank=True) 
    tags = TaggableManager() # Add tagging functionality 
    def __str__(self):
	    return self.title + ' | ' + str(self.author)

    
''' Model to rapresent a category for blog posts '''
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name