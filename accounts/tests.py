from django.test import TestCase
from django.contrib.auth import get_user_model


class UserAccountModelTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(username="eddy", password="password")
        self.assertEqual(user.username, "eddy")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username="admin", password="password"
        )
        self.assertTrue(admin_user.is_superuser)
