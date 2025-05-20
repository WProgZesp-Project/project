from django.urls import path
from .views.index_view import index
from .views.registration import UserRegistrationView, activate
from .views.login import UserLoginView
from .views.logout import UserLogoutView
from .views.merge_pdf_view import merge_pdfs

urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
]
