from django.urls import path
from .views.index_view import index
from .views.merge_pdf_view import merge_pdfs

urlpatterns = [
    path('', index, name='index'),
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
]
