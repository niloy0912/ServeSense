from django.urls import path
from . import views

urlpatterns = [
    path('', views.table_list, name='table_list'),
    path('edit/<int:pk>/', views.table_edit, name='table_edit'),
    path('delete/<int:pk>/', views.table_delete, name='table_delete'),
]
