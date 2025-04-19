from django.urls import path
from .views.index_view import index
from .views.registration import UserRegistrationView

urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
]
