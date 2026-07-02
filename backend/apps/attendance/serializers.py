from rest_framework import serializers
from .models import AttendanceRecord, AbsenceJustification


class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    worked_hours = serializers.ReadOnlyField()

    class Meta:
        model = AttendanceRecord
        fields = [
            'id', 'company', 'employee', 'employee_name', 'date',
            'check_in', 'check_in_lat', 'check_in_lng', 'check_in_source',
            'is_late', 'late_minutes',
            'check_out', 'check_out_lat', 'check_out_lng',
            'left_early', 'early_minutes', 'worked_hours',
            'recorded_by', 'notes', 'created_at',
        ]
        read_only_fields = ['id', 'company', 'created_at']


class AbsenceJustificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsenceJustification
        fields = '__all__'
        read_only_fields = ['id', 'status', 'reviewed_by']
