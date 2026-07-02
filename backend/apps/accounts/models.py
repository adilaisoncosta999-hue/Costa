import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Utilizador do sistema. O papel (role) define o nível de acesso."""

    ROLE_CHOICES = (
        ('super_admin', 'Super Administrador'),   # dono do SaaS, vê todas as empresas
        ('company_admin', 'Administrador da Empresa'),
        ('hr', 'Recursos Humanos'),
        ('supervisor', 'Supervisor'),
        ('employee', 'Funcionário'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    company = models.ForeignKey(
        'companies.Company', on_delete=models.CASCADE,
        related_name='users', null=True, blank=True,
        help_text='Vazio apenas para super_admin'
    )
    phone = models.CharField(max_length=30, blank=True)
    language = models.CharField(max_length=5, choices=(('pt', 'Português'), ('en', 'English')), default='pt')
    is_company_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    @property
    def is_super_admin(self):
        return self.role == 'super_admin'

    @property
    def is_company_admin(self):
        return self.role == 'company_admin'
