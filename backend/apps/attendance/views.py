from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.employees.models import Employee
from apps.companies.mixins import CompanyScopedMixin
from .models import AttendanceRecord, AbsenceJustification
from .serializers import AttendanceRecordSerializer, AbsenceJustificationSerializer


class AttendanceRecordViewSet(CompanyScopedMixin, viewsets.ModelViewSet):
    queryset = AttendanceRecord.objects.select_related('employee').all()
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['employee', 'date', 'is_late', 'left_early']


class QRScanCheckInOutView(APIView):
    """
    POST /api/attendance/scan/
    Body: { "qr_token": "<uuid lido da câmara>", "latitude": -8.83, "longitude": 13.23 }

    Lógica:
      - Se o funcionário ainda não tem registo hoje -> cria check-in.
      - Se já tem check-in mas não tem check-out -> regista check-out.
      - Se já tem os dois -> devolve erro (já concluiu o dia).
    Calcula automaticamente atrasos e saídas antecipadas com base no WorkSchedule.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        qr_token = request.data.get('qr_token')
        lat = request.data.get('latitude')
        lng = request.data.get('longitude')

        if not qr_token:
            return Response({'detail': 'qr_token é obrigatório.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.select_related('schedule', 'company').get(qr_token=qr_token)
        except Employee.DoesNotExist:
            return Response({'detail': 'Funcionário não encontrado para este QR Code.'},
                             status=status.HTTP_404_NOT_FOUND)

        # Garante que o utilizador autenticado pertence à mesma empresa do funcionário
        user = request.user
        if not user.is_super_admin and user.company_id != employee.company_id:
            return Response({'detail': 'Sem permissão para marcar presença nesta empresa.'},
                             status=status.HTTP_403_FORBIDDEN)

        now = timezone.localtime()
        today = now.date()

        record, _ = AttendanceRecord.objects.get_or_create(
            employee=employee, date=today,
            defaults={'company': employee.company}
        )

        schedule = employee.schedule

        if not record.check_in:
            record.check_in = now
            record.check_in_source = 'qr_scan'
            record.check_in_lat = lat
            record.check_in_lng = lng
            record.recorded_by = user

            if schedule:
                expected_start = datetime.combine(today, schedule.start_time, tzinfo=now.tzinfo)
                tolerance = timedelta(minutes=schedule.tolerance_minutes)
                if now > expected_start + tolerance:
                    record.is_late = True
                    record.late_minutes = int((now - expected_start).total_seconds() // 60)

            record.save()
            action_taken = 'check_in'

        elif not record.check_out:
            record.check_out = now
            record.check_out_lat = lat
            record.check_out_lng = lng

            if schedule:
                expected_end = datetime.combine(today, schedule.end_time, tzinfo=now.tzinfo)
                if now < expected_end:
                    record.left_early = True
                    record.early_minutes = int((expected_end - now).total_seconds() // 60)

            record.save()
            action_taken = 'check_out'

        else:
            return Response(
                {'detail': 'Este funcionário já registou entrada e saída hoje.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response({
            'action': action_taken,
            'employee': employee.full_name,
            'employee_number': employee.employee_number,
            'time': now.isoformat(),
            'is_late': record.is_late,
            'late_minutes': record.late_minutes,
            'left_early': record.left_early,
            'record': AttendanceRecordSerializer(record).data,
        }, status=status.HTTP_200_OK)


class AbsenceJustificationViewSet(viewsets.ModelViewSet):
    queryset = AbsenceJustification.objects.select_related('employee').all()
    serializer_class = AbsenceJustificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.is_super_admin:
            return qs
        return qs.filter(employee__company=user.company)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """POST /api/attendance/justifications/{id}/review/  body: {"status": "approved"}"""
        justification = self.get_object()
        new_status = request.data.get('status')
        if new_status not in ('approved', 'rejected'):
            return Response({'detail': 'status deve ser approved ou rejected.'}, status=400)
        justification.status = new_status
        justification.reviewed_by = request.user
        justification.save()
        return Response(AbsenceJustificationSerializer(justification).data)
