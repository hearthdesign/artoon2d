from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager

# -------------------------------------------------
# Category
# -------------------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_posts', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.name


# -------------------------------------------------
# Profile
# -------------------------------------------------
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    visitor_count = models.PositiveIntegerField(default=0)

    def toggle_follow(self, target_profile):
        
        #Toggle follow/unfollow. 
        # Returns: 'followed', 'unfollowed', or 'self'
        if self == target_profile:
            return 'self'

        follow, created = Follow.objects.get_or_create(
            from_profile=self,
            to_profile=target_profile
        )

        if not created:
            follow.delete()
            return 'unfollowed'

        return 'followed'

    def is_following(self, target_profile):
        return Follow.objects.filter(
            from_profile=self,
            to_profile=target_profile
        ).exists()

    def __str__(self):
        return f"{self.user.username}'s profile"


# -------------------------------------------------
# Follow relationship
# -------------------------------------------------
class Follow(models.Model):
    from_profile = models.ForeignKey(
        Profile,
        related_name='following_relations',
        on_delete=models.CASCADE
    )
    to_profile = models.ForeignKey(
        Profile,
        related_name='follower_relations',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_profile', 'to_profile')
        indexes = [
            models.Index(fields=['from_profile', 'to_profile']),
            models.Index(fields=['to_profile']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_profile.user.username} → {self.to_profile.user.username}"


# -------------------------------------------------
# Post
# -------------------------------------------------
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True
    )
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        editable=False
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts'
    )

    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)

    tags = TaggableManager(blank=True)

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # -----------------------------
    # Auto-generated slug
    # -----------------------------
    def save(self, *args, **kwargs):
        if not self.slug or self.pk and Post.objects.filter(pk=self.pk, title__ne=self.title):
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    # -----------------------------
    # Likes
    # -----------------------------
    def toggle_like(self, user):
        if self.likes.filter(pk=user.pk).exists():
            self.likes.remove(user)
            return 'unliked'
        self.likes.add(user)
        return 'liked'

    def __str__(self):
        return f"{self.title} | {self.author.username}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['category']),
        ]

# -------------------------------------------------
# Visitor Counter (Singleton)
# -------------------------------------------------
class VisitorCounter(models.Model):
    total_visits = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Visitor Counter"
        verbose_name_plural = "Visitor Counter"

    def __str__(self):
        return f"Total visits: {self.total_visits}"
