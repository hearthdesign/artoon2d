from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    featured_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    theme = models.CharField(max_length=50)
  
    def __str__(self):
	    return self.title + ' | ' + str(self.author)

    
