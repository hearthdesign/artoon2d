# Django admin configuration file
from django.contrib import admin
'''Connection to Post model'''
from .models import Post

''' Admin Class to manage Post model in the admin interface '''
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'theme', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('theme', 'author')

admin.site.register(Post, PostAdmin)