import pytest
from django.contrib.auth.models import User
from artoon2d_blog.models import Post

@pytest.mark.django_db
def test_post_creation():
    user = User.objects.create_user(username="author", password="pass")
    post = Post.objects.create(title="Hello", content="World", author=user)
    
    assert post.title == "Hello"
    assert post.author == user
    assert post.slug != ""  # Slug auto-generated

