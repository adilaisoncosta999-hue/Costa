from django.contrib import admin
from .models import AttendanceRecord, AbsenceJustification

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'is_late', 'left_early')
    list_filter = ('company', 'date', 'is_late', 'left_early')
    search_fields = ('employee__full_name',)

@admin.register(AbsenceJustification)
class AbsenceJustificationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'status', 'reviewed_by')
    list_filter = ('status',)
