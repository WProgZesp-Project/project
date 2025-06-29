from django.test import SimpleTestCase, RequestFactory
from django.urls import reverse, resolve
from pdfhandler.views.index_view import index
from pdfhandler.views.merge_pdf import merge_pdfs, merge_form, merge_result
from pdfhandler.views.split import SplitPDFTemplateView, SplitPDFView
from pdfhandler.views.registration import UserRegistrationView, RegistrationSuccessView
from pdfhandler.views.remove_password_view import remove_pdf_password, remove_password_page
from pdfhandler.views.remove_pdf_pages_view import remove_pdf_pages, remove_pdf_pages_view
from pdfhandler.views.login import UserLoginView
from pdfhandler.views.logout import UserLogoutView
from pdfhandler.views.extract_pdf_view import ExtractPagesView
from pdfapp.pdfhandler.views.operation_history import history_fragment, history_page
from pdfhandler.views.dashboard_view import DashboardView


class SimpleURLTestCase(SimpleTestCase):
    def test_url_resolution(self):
        """Test URL configuration resolves to correct views"""
        # Function-based views
        self.assertEqual(resolve(reverse('index')).func.view_class, DashboardView)
        self.assertEqual(resolve(reverse('merge_form')).func, merge_form)
        self.assertEqual(resolve(reverse('merge_result')).func, merge_result)
        self.assertEqual(resolve(reverse('merge_pdfs')).func, merge_pdfs)
        self.assertEqual(resolve(reverse('remove_password_page')).func, remove_password_page)
        self.assertEqual(resolve(reverse('remove_pdf_password')).func, remove_pdf_password)
        self.assertEqual(resolve(reverse('remove_pdf_pages_view')).func, remove_pdf_pages_view)
        self.assertEqual(resolve(reverse('remove_pdf_pages')).func, remove_pdf_pages)
        self.assertEqual(resolve(reverse('history')).func, history_page)
        self.assertEqual(resolve(reverse('history_fragment')).func, history_fragment)

        # Class-based views
        self.assertEqual(resolve(reverse('register')).func.view_class, UserRegistrationView)
        self.assertEqual(resolve(reverse('registration_success')).func.view_class, RegistrationSuccessView)
        self.assertEqual(resolve(reverse('login')).func.view_class, UserLoginView)
        self.assertEqual(resolve(reverse('logout')).func.view_class, UserLogoutView)
        self.assertEqual(resolve(reverse('extract-pages')).func.view_class, ExtractPagesView)
        self.assertEqual(resolve(reverse('split_pdf_page')).func.view_class, SplitPDFTemplateView)
        self.assertEqual(resolve(reverse('split_pdf')).func.view_class, SplitPDFView)


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
        self.assertEqual(response.status_code, 405)
