from django.contrib import admin
from .models import Company, Department, Position, WorkSchedule

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'plan', 'is_active', 'max_employees', 'created_at')
    list_filter = ('plan', 'is_active')
    search_fields = ('name', 'nif')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company')
    list_filter = ('company',)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'company')
    list_filter = ('company', 'department')

@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'start_time', 'end_time', 'tolerance_minutes')
