from . import views
from django.urls import path

urlpatterns = [
    path('', views.view_all_classes, name="classes"),
    path('create/', views.create_class, name="create_class"),
    path('<str:pk>/', views.view_class, name="class"),
    path('<str:pk>/remove/<str:prn>', views.remove_member, name="remove_member"),
    path('edit/<str:pk>/', views.edit_class, name="edit_class"),
    path('delete/<str:pk>/', views.delete_class, name="delete_class"),
    path('<str:pk>/lectures/create/', views.create_lecture, name="create_lecture"),
    path('<str:pk>/lectures/<int:no>', views.view_lecture, name="lecture"),
    path('<str:pk>/lectures/delete/<int:no>',
         views.delete_lecture, name="delete_lecture"),
    path('<str:pk>/lectures/<int:no>/attendance/detect/',
         views.detect_attendance, name="detect_attendance"),
    path('<str:pk>/lectures/<int:no>/attendance/edit/<str:prn>/',
         views.edit_attendance, name="edit_attendance"),
]
