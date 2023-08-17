from . import views
from django.urls import path

urlpatterns = [
    path('timetable/<str:date>/', views.get_timetable),
    path('search/<str:query>/', views.get_search),
]
