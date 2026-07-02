from rest_framework import viewsets, permissions
from .models import Company, Department, Position, WorkSchedule
from .serializers import CompanySerializer, DepartmentSerializer, PositionSerializer, WorkScheduleSerializer
from .mixins import CompanyScopedMixin


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_super_admin)


class CompanyViewSet(viewsets.ModelViewSet):
    """Apenas o Super Admin gere as empresas clientes do SaaS."""
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsSuperAdmin]


class DepartmentViewSet(CompanyScopedMixin, viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class PositionViewSet(CompanyScopedMixin, viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]


class WorkScheduleViewSet(CompanyScopedMixin, viewsets.ModelViewSet):
    queryset = WorkSchedule.objects.all()
    serializer_class = WorkScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
