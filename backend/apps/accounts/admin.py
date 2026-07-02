from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CWMUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'company', 'is_active')
    list_filter = ('role', 'company', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('CWM', {'fields': ('role', 'company', 'phone', 'language')}),
    )
