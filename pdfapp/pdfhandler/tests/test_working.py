from django.test import TestCase, Client
from django.urls import reverse, resolve
from django.utils import timezone
from django.contrib.auth import get_user_model
from pdfhandler.models import MergeHistory
from pdfhandler.views.index_view import index
from pdfhandler.views.merge_pdf_view import merge_pdfs

User = get_user_model()

class MergeHistoryTestCase(TestCase):
    def test_create_merge_history(self):
        """Test creating a MergeHistory record"""
        merge_history = MergeHistory.objects.create(
            filenames="file1.pdf,file2.pdf",
            merged_filename="merged_123456.pdf"
        )
        self.assertEqual(MergeHistory.objects.count(), 1)
        self.assertEqual(merge_history.filenames, "file1.pdf,file2.pdf")
        self.assertEqual(merge_history.merged_filename, "merged_123456.pdf")
        self.assertIsNotNone(merge_history.timestamp)

class UserModelTestCase(TestCase):
    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="securepassword123"
        )
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("securepassword123"))

class MergePDFTestCase(TestCase):
    def test_merge_pdf_endpoint_requires_post(self):
        """Test merge_pdfs endpoint requires POST method"""
        client = Client()
        url = reverse('merge_pdfs')
        response = client.get(url)
        self.assertEqual(response.status_code, 405)  # Method not allowed
        
class URLConfigTestCase(TestCase):
    def test_url_resolution(self):
        """Test URL configuration resolves to correct views"""
        # Test index URL
        url = reverse('index')
        self.assertEqual(url, '/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, index)
        
        # Test merge_pdfs URL
        url = reverse('merge_pdfs')
        self.assertEqual(url, '/api/merge-pdfs/')
        resolver = resolve(url)
        self.assertEqual(resolver.func, merge_pdfs) 