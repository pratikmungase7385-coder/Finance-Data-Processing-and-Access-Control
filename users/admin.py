from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


# 🔥 CREATE FORM
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'full_name')


# 🔥 UPDATE FORM
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'full_name', 'role', 'is_staff')


# 🔥 ADMIN CONFIG
class CustomUserAdmin(BaseUserAdmin):
    model = User

    add_form = CustomUserCreationForm   # 🔥 IMPORTANT
    form = CustomUserChangeForm         # 🔥 IMPORTANT

    list_display = ('email', 'full_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

    ordering = ('email',)
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'role', 'is_staff'),
        }),
    )

    filter_horizontal = ()


admin.site.register(User, CustomUserAdmin)