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
    featured_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True) 
    tags = TaggableManager() # Add tagging functionality 
    def __str__(self):
	    return self.title + ' | ' + str(self.author)

    
