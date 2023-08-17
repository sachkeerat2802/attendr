from . import views
from django.urls import path

urlpatterns = [
    path('add/', views.add_user, name="add_user"),
    path('edit/<str:pk>/', views.edit_user, name="edit_user"),
    path('<str:pk>/', views.view_user, name="user"),
]
