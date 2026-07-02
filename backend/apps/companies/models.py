import uuid
from django.db import models


class Company(models.Model):
    """Cada empresa cliente do SaaS. Todos os dados são isolados por empresa."""

    PLAN_CHOICES = (
        ('trial', 'Trial'),
        ('basic', 'Básico'),
        ('pro', 'Profissional'),
        ('enterprise', 'Empresarial'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('Nome da empresa', max_length=150)
    nif = models.CharField('NIF / Identificação fiscal', max_length=30, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)

    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='trial')
    is_active = models.BooleanField(default=True)
    max_employees = models.PositiveIntegerField(default=20)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['name']

    def __str__(self):
        return self.name


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'
        unique_together = ('company', 'name')

    def __str__(self):
        return f'{self.name} ({self.company.name})'


class Position(models.Model):
    """Cargo / função do funcionário."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='positions')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='positions')
    title = models.CharField('Cargo', max_length=100)

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return self.title


class WorkSchedule(models.Model):
    """Horário de trabalho padrão de uma empresa/departamento."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='schedules')
    name = models.CharField(max_length=100, default='Horário padrão')
    start_time = models.TimeField(default='08:00')
    end_time = models.TimeField(default='17:00')
    tolerance_minutes = models.PositiveIntegerField('Tolerância de atraso (min)', default=10)
    works_saturday = models.BooleanField(default=False)
    works_sunday = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Horário de Trabalho'
        verbose_name_plural = 'Horários de Trabalho'

    def __str__(self):
        return f'{self.name} - {self.company.name}'
