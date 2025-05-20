from django.test import SimpleTestCase, RequestFactory
from django.urls import reverse, resolve
from pdfhandler.views.index_view import index
from pdfhandler.views.merge_pdf_view import merge_pdfs


class SimpleURLTestCase(SimpleTestCase):
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


class ViewResponseTestCase(SimpleTestCase):
    def test_index_view_returns_200(self):
        """Test index view returns 200 status code"""
        factory = RequestFactory()
        request = factory.get('/')
        response = index(request)
        self.assertEqual(response.status_code, 200)


class MergePDFMethodTestCase(SimpleTestCase):
    def test_merge_pdf_endpoint_requires_post(self):
        """Test merge_pdfs endpoint rejects GET requests"""
        factory = RequestFactory()
        request = factory.get('/api/merge-pdfs/')
        response = merge_pdfs(request)
        self.assertEqual(response.status_code, 405)  # Method not allowed 