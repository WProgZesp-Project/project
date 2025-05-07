from django.urls import path
from .views.index_view import index
from .views.registration import UserRegistrationView, activate

urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate')
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
]
