from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.registration import (
    UserRegistrationView, RegistrationSuccessView, activate
)
from .views.remove_password_view import (
    remove_pdf_password, remove_password_page
)
from .views.remove_pdf_pages_view import (
    remove_pdf_pages, remove_pdf_pages_view
)
from pdfhandler.views.password_reset_views import (
    PasswordResetView,
    PasswordResetSentView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views.split import SplitPDFView, SplitPDFTemplateView
from .views.merge_pdf import merge_pdfs, merge_form, merge_result
from .views.login import UserLoginView
from .views.logout import LogoutView 

from .views.extract_pdf_view import ExtractPagesView
from .views.operation_history_view import history_fragment, history_page
from .views.dashboard_view import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
    path('merge/', merge_form, name='merge_form'),
    path('merge/result/', merge_result, name='merge_result'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path(
        'register/success/',
        RegistrationSuccessView.as_view(),
        name='registration_success'
    ),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('remove-password/', remove_password_page, name='remove_password_page'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/sent/', PasswordResetSentView.as_view(), name='password_reset_sent'),
    path(
        'password-reset/confirm/<str:uidb64>/<str:token>/', 
        PasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'
    ),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(
        'remove-password/api/',
        remove_pdf_password,
        name='remove_pdf_password'
    ),
    path('remove-pages/', remove_pdf_pages_view, name='remove_pdf_pages_view'),
    path(
        'remove-pages/api/',
        remove_pdf_pages,
        name='remove_pdf_pages'
    ),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
    path('api/extract-pages', ExtractPagesView.as_view(), name='extract-pages'),
    path('history/', history_page, name='history'),
    path('history/fragment/', history_fragment, name='history_fragment'),
    path('split/', SplitPDFTemplateView.as_view(), name='split_pdf_page'),
    path("api/split/", SplitPDFView.as_view(), name="split_pdf"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
