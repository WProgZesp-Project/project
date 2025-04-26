from django.urls import path
from .views.index_view import index
from .views.registration import UserRegistrationView, activate
from .views.login import UserLoginView
from .views.remove_password_view import remove_pdf_password, remove_password_page
from .views.merge_pdf_view import merge_pdfs

urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('remove-password/', remove_password_page, name='remove_password_page'),
    path('api/remove-password/', remove_pdf_password, name='remove_pdf_password'),
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
]
