from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'uid')}),
        ('Permissions', {'fields': (
            'is_staff',
            'is_superuser',
            'is_active',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'name', 'uid')
            }
        ),
    )

    list_display = ('email', 'name',
                    'is_staff', 'uid')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
