import io
from datetime import date
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from apps.employees.models import Employee
from .models import AttendanceRecord


def _scope_company(request):
    """Devolve a empresa do utilizador (ou None se super_admin sem filtro)."""
    return None if request.user.is_super_admin else request.user.company


class DashboardStatsView(APIView):
    """
    GET /api/attendance/dashboard/?date=2026-06-30
    Estatísticas em tempo real para o painel administrativo.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        target_date = request.query_params.get('date') or timezone.localdate().isoformat()
        company = _scope_company(request)

        employees = Employee.objects.filter(status='active')
        records = AttendanceRecord.objects.filter(date=target_date)
        if company:
            employees = employees.filter(company=company)
            records = records.filter(company=company)

        total_employees = employees.count()
        present_today = records.filter(check_in__isnull=False).count()
        late_today = records.filter(is_late=True).count()
        left_early_today = records.filter(left_early=True).count()
        absent_today = total_employees - present_today

        return Response({
            'date': target_date,
            'total_employees': total_employees,
            'present_today': present_today,
            'absent_today': max(absent_today, 0),
            'late_today': late_today,
            'left_early_today': left_early_today,
            'attendance_rate': round((present_today / total_employees) * 100, 1) if total_employees else 0,
        })


class AttendanceReportExportView(APIView):
    """
    GET /api/attendance/reports/export/?format=pdf&start=2026-06-01&end=2026-06-30&employee=<id>
    Exporta relatório de assiduidade em PDF ou Excel.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        fmt = request.query_params.get('format', 'excel')
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        employee_id = request.query_params.get('employee')
        company = _scope_company(request)

        qs = AttendanceRecord.objects.select_related('employee').all()
        if company:
            qs = qs.filter(company=company)
        if start:
            qs = qs.filter(date__gte=start)
        if end:
            qs = qs.filter(date__lte=end)
        if employee_id:
            qs = qs.filter(employee_id=employee_id)
        qs = qs.order_by('employee__full_name', 'date')

        rows = [
            [
                r.employee.full_name,
                r.employee.employee_number,
                r.date.isoformat(),
                r.check_in.strftime('%H:%M') if r.check_in else '-',
                r.check_out.strftime('%H:%M') if r.check_out else '-',
                'Sim' if r.is_late else 'Não',
                'Sim' if r.left_early else 'Não',
                str(r.worked_hours) if r.worked_hours else '-',
            ]
            for r in qs
        ]
        headers = ['Funcionário', 'Nº', 'Data', 'Entrada', 'Saída', 'Atraso', 'Saída Antecipada', 'Horas']

        if fmt == 'pdf':
            return self._export_pdf(headers, rows)
        return self._export_excel(headers, rows)

    def _export_excel(self, headers, rows):
        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        ws.title = 'Assiduidade'
        ws.append(headers)
        for row in rows:
            ws.append(row)

        buffer = io.BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        response = HttpResponse(
            buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename=relatorio_assiduidade_{date.today()}.xlsx'
        return response

    def _export_pdf(self, headers, rows):
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
        styles = getSampleStyleSheet()
        elements = [Paragraph('Costa Workforce Manager - Relatório de Assiduidade', styles['Title'])]

        data = [headers] + rows
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0A1F44')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F0F0F0')]),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=relatorio_assiduidade_{date.today()}.pdf'
        return response
