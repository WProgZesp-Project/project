from django.test import TestCase
from pdfhandler.models import User

class AddUserTestCase(TestCase):
    def test_create_user(self):
        user = User(username='test', email='test@example.com')
        user.save()
        self.assertEqual(User.objects.count(), 1)