from django.urls import path
from .views.index_view import index
from .views.registration import UserRegistrationView, activate
from .views.login import UserLoginView

urlpatterns = [
    path('', index, name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]
