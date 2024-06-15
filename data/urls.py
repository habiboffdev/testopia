# data/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file, name='upload_file'),
    path('test/<int:id>/', views.solve_test, name='solve_test')
]