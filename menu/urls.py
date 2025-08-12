from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('edit/<int:pk>/', views.menu_edit, name='menu_edit'),
    path('delete/<int:pk>/', views.menu_delete, name='menu_delete'),
]
