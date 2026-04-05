from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'full_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

    ordering = ('email',)
    search_fields = ('email',)

    # 🔥 IMPORTANT
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser')}),
    )

    # 🔥 THIS FIXES 500 ERROR
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role', 'is_staff'),
        }),
    )

    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)