from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Employee
from .serializers import EmployeeSerializer
from apps.companies.mixins import CompanyScopedMixin


class EmployeeViewSet(CompanyScopedMixin, viewsets.ModelViewSet):
    """
    CRUD de funcionários. Isolado por empresa automaticamente.
    Suporta upload de fotografia (multipart/form-data).
    """
    queryset = Employee.objects.select_related('department', 'position', 'company').all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    filterset_fields = ['department', 'position', 'status']
    search_fields = ['full_name', 'employee_number']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
