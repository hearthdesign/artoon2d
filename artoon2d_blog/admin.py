# Django admin configuration file
from django.contrib import admin
# Connection to Post model
from .models import Post

# Admin Class to manage Post model in the admin interface


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Main Content',
            { 'fields': ('title', 'content', 'image')
        }),
        ('Classification', {
              'fields': ('theme', 'category', 'tags')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at',)
        }), 
    )
    readonly_fields = ('author', 'created_at', 'updated_at')
    list_display = (
        'id', 'title', 'author', 'theme', 'category', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('theme', 'author', 'category')
    list_select_related = ('author', 'category')

    
    def save_model(self, request, obj, form, change): 
        if not obj.pk: 
            obj.author = request.user 
        super().save_model(request, obj, form, change)

