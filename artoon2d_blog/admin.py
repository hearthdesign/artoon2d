# Django admin configuration file
from django.contrib import admin
'''Connection to Post model'''
from .models import Post

''' Admin Class to manage Post model in the admin interface '''


@admin.register(Post) 
class PostAdmin(admin.ModelAdmin): 
    fields = ('title', 'content', 'image', 'theme')
    list_display = ('id', 'title', 'author', 'theme', 'created_at') 
    search_fields = ('title', 'content') 
    list_filter = ('theme', 'author') 

    
    def get_readonly_fields(self, request, obj=None): # Superusers can edit the author 
        if request.user.is_superuser: 
            return ()
        # Staff users cannot edit the author 
        return ('author',) 

    def save_model(self, request, obj, form, change): 
        # If creating a new post set author automatically 
        if not obj.pk: 
            obj.author = request.user 
        super().save_model(request, obj, form, change)