from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.merge_page, name='merge_page'),
    path('upload/', views.upload_files, name='upload_files'),
    path('merge/', views.merge_files, name='merge_files'),
    path('reorder/<str:direction>/<int:index>/', views.reorder, name='reorder'),
    path('delete/<int:index>/', views.delete_file, name='delete_file'),
]
