from django.test import TestCase
from django.contrib.auth.models import User
from artoon2d_blog.models import Profile, Follow

class FollowToggleTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create_user(username='u1', password='pass')
        cls.user2 = User.objects.create_user(username='u2', password='pass')
        cls.profile1 = cls.user1.profile
        cls.profile2 = cls.user2.profile

    def test_toggle_follow(self):
        """Following toggles correctly"""
        result1 = self.profile1.toggle_follow(self.profile2)
        self.assertEqual(result1, 'followed')
        self.assertTrue(Follow.objects.filter(from_profile=self.profile1, to_profile=self.profile2).exists())

        result2 = self.profile1.toggle_follow(self.profile2)
        self.assertEqual(result2, 'unfollowed')
        self.assertFalse(Follow.objects.filter(from_profile=self.profile1, to_profile=self.profile2).exists())
