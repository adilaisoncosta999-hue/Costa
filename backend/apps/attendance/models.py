import uuid
from django.db import models
from django.utils import timezone


class AttendanceRecord(models.Model):
    """Um registo de presença diário de um funcionário (check-in / check-out)."""

    SOURCE_CHOICES = (
        ('qr_scan', 'Leitura QR Code'),
        ('manual', 'Marcação manual'),
        ('face_recognition', 'Reconhecimento facial'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('companies.Company', on_delete=models.CASCADE, related_name='attendance_records')
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.localdate)

    check_in = models.DateTimeField(null=True, blank=True)
    check_in_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_in_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_in_source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default='qr_scan')
    is_late = models.BooleanField(default=False)
    late_minutes = models.PositiveIntegerField(default=0)

    check_out = models.DateTimeField(null=True, blank=True)
    check_out_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    check_out_lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    left_early = models.BooleanField(default=False)
    early_minutes = models.PositiveIntegerField(default=0)

    # Quem fez a marcação (ex: supervisor que leu o QR code do funcionário)
    recorded_by = models.ForeignKey(
        'accounts.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='recorded_attendances'
    )

    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Registo de Presença'
        verbose_name_plural = 'Registos de Presença'
        unique_together = ('employee', 'date')
        ordering = ['-date']

    def __str__(self):
        return f'{self.employee.full_name} - {self.date}'

    @property
    def worked_hours(self):
        if self.check_in and self.check_out:
            delta = self.check_out - self.check_in
            return round(delta.total_seconds() / 3600, 2)
        return None


class AbsenceJustification(models.Model):
    """Justificação de falta enviada pelo funcionário ou registada pelo RH."""

    STATUS_CHOICES = (
        ('pending', 'Pendente'),
        ('approved', 'Aprovada'),
        ('rejected', 'Rejeitada'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='justifications')
    date = models.DateField()
    reason = models.TextField()
    attachment = models.FileField(upload_to='justifications/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Justificação de Falta'
        verbose_name_plural = 'Justificações de Falta'

    def __str__(self):
        return f'{self.employee.full_name} - {self.date} ({self.get_status_display()})'
