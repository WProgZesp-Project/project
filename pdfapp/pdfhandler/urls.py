from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views.index_view import index
from .views.merge_pdf import merge_pdfs, merge_form, merge_result
from .views.registration import UserRegistrationView, activate
from .views.split import SplitPDFView, SplitPDFTemplateView

urlpatterns = [
    path('', index, name='index'),
    path('merge/', merge_form, name='merge_form'),
    path('merge/result/', merge_result, name='merge_result'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('api/merge-pdfs/', merge_pdfs, name='merge_pdfs'),
    path('split/', SplitPDFTemplateView.as_view(), name='split_pdf_page'),
    path("api/split/", SplitPDFView.as_view(), name="split_pdf"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
