from django.urls import path
from .views.index_view import index
from .views.registration import UserRegistrationView, RegistrationSuccessView, activate
from .views.registration import UserRegistrationView, activate
from .views.remove_password_view import remove_pdf_password
from .views.remove_password_view import remove_password_page
from .views.merge_pdf_view import merge_pdfs
from .views.login import UserLoginView
from .views.logout import UserLogoutView


urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/success/', RegistrationSuccessView.as_view(), name='registration_success'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('remove-password/', remove_password_page, name='remove_password_page'),
    path(
        'remove-password/api/',
        remove_pdf_password,
        name='remove_pdf_password'
    ),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
]
