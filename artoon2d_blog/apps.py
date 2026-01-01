from django.apps import AppConfig


class Artoon2DBlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'artoon2d_blog'

    def ready(self):
        import artoon2d_blog.signals
