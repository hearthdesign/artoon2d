# prevents double-like issues
import pytest
from django.contrib.auth.models import User
from artoon2d_blog.models import Post

@pytest.mark.django_db
def test_toggle_like():
    # Create a user and a post
    user = User.objects.create_user(username="tester", password="pass")
    post = Post.objects.create(title="Test Post", content="Content", author=user)
    
    # Initially no likes
    assert post.likes.count() == 0

    # User likes the post
    action1 = post.toggle_like(user)
    assert action1 == "liked"
    assert post.likes.count() == 1

    # User tries to like again (should unlike)
    action2 = post.toggle_like(user)
    assert action2 == "unliked"
    assert post.likes.count() == 0
