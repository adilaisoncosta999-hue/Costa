from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'employee_number', 'company', 'department', 'position', 'status')
    list_filter = ('company', 'department', 'status')
    search_fields = ('full_name', 'employee_number', 'email')
    readonly_fields = ('qr_token', 'qr_code_image')
