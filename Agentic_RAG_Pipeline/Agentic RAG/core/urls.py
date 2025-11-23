from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/query/', views.process_query, name='process_query'),
    path('api/upload/', views.upload_document, name='upload_document'),
]