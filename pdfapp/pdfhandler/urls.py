from django.urls import path
from .views.index_view import index

urlpatterns = [
    path('', index, name='index'),
]
