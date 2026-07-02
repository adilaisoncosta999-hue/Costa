from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, CWMTokenObtainPairSerializer


class CWMLoginView(TokenObtainPairView):
    """POST /api/auth/login/  ->  { access, refresh, user }"""
    serializer_class = CWMTokenObtainPairSerializer


class IsCompanyAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and (u.is_super_admin or u.is_company_admin or u.role == 'hr'))


class UserViewSet(viewsets.ModelViewSet):
    """
    Gestão de utilizadores. Isola automaticamente por empresa,
    exceto para o super_admin que vê todas.
    """
    serializer_class = UserSerializer
    permission_classes = [IsCompanyAdminOrSuperAdmin]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_super_admin:
            return User.objects.all()
        return User.objects.filter(company=user.company)

    def perform_create(self, serializer):
        user = self.request.user
        if user.is_super_admin:
            serializer.save()
        else:
            serializer.save(company=user.company)
