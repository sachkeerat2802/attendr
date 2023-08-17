from django.contrib import admin
from .models import UserProfile, StaffProfile

admin.site.register(UserProfile)
admin.site.register(StaffProfile)
