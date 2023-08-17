from django.contrib import admin
from .models import Class, Lecture, Attendance

admin.site.register(Class)
admin.site.register(Lecture)
admin.site.register(Attendance)
