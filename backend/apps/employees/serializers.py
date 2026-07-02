from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    position_title = serializers.CharField(source='position.title', read_only=True)
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'company', 'user', 'employee_number', 'full_name', 'photo',
            'department', 'department_name', 'position', 'position_title',
            'schedule', 'email', 'phone', 'hire_date', 'status',
            'qr_code_url', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'company', 'qr_token', 'created_at', 'updated_at']

    def get_qr_code_url(self, obj):
        request = self.context.get('request')
        if obj.qr_code_image and request:
            return request.build_absolute_uri(obj.qr_code_image.url)
        return None


class EmployeeQRLookupSerializer(serializers.Serializer):
    """Usado pelo scanner: recebe o token lido do QR Code."""
    qr_token = serializers.UUIDField()
    latitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
    longitude = serializers.DecimalField(max_digits=9, decimal_places=6, required=False)
