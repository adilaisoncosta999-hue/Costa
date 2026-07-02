import uuid
from django.db import models


def employee_photo_path(instance, filename):
    return f'employees/{instance.company_id}/{instance.id}_{filename}'


def employee_qr_path(instance, filename):
    return f'qrcodes/{instance.company_id}/{instance.id}.png'


class Employee(models.Model):
    STATUS_CHOICES = (
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
        ('on_leave', 'Em licença'),
        ('terminated', 'Desligado'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='employees')
    user = models.OneToOneField(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='employee_profile',
        help_text='Conta de login associada (opcional para funcionários sem acesso à app)'
    )

    employee_number = models.CharField('Número de funcionário', max_length=30)
    full_name = models.CharField('Nome completo', max_length=150)
    photo = models.ImageField(upload_to=employee_photo_path, blank=True, null=True)
    department = models.ForeignKey('companies.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    position = models.ForeignKey('companies.Position', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    schedule = models.ForeignKey('companies.WorkSchedule', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')

    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    # Identificação para o scanner QR (código único e secreto, não é o ID público)
    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    qr_code_image = models.ImageField(upload_to=employee_qr_path, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        unique_together = ('company', 'employee_number')
        ordering = ['full_name']

    def __str__(self):
        return f'{self.full_name} - {self.company.name}'

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new or not self.qr_code_image:
            self.generate_qr_code()

    def generate_qr_code(self):
        """Gera a imagem do QR Code com base no qr_token e guarda no campo qr_code_image."""
        import qrcode
        from io import BytesIO
        from django.core.files.base import ContentFile

        payload = str(self.qr_token)
        img = qrcode.make(payload)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f'{self.id}.png'
        self.qr_code_image.save(filename, ContentFile(buffer.getvalue()), save=False)
        super().save(update_fields=['qr_code_image'])
