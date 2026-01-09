from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from artoon2d_blog.models import Post

class PostDeleteTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='author', password='pass')
        cls.post = Post.objects.create(
            title="Delete Me",
            content="Content",
            author=cls.user
        )

    def test_post_deletion_removes_from_list(self):
        """After deletion, post is gone from post list."""
        self.client.login(username='author', password='pass')
        delete_url = reverse('post_delete', args=[self.post.pk])
        
        # Perform deletion
        response = self.client.post(delete_url, follow=True)
        self.assertRedirects(response, reverse('post_list'))

        # Check DB
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

        # Check post_list view context
        list_url = reverse('post_list')
        response2 = self.client.get(list_url)
        self.assertNotContains(response2, "Delete Me")
