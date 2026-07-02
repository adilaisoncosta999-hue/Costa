from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AttendanceRecordViewSet, QRScanCheckInOutView, AbsenceJustificationViewSet
from .reports import DashboardStatsView, AttendanceReportExportView

router = DefaultRouter()
router.register('records', AttendanceRecordViewSet, basename='attendance-record')
router.register('justifications', AbsenceJustificationViewSet, basename='justification')

urlpatterns = router.urls + [
    path('scan/', QRScanCheckInOutView.as_view(), name='attendance-scan'),
    path('dashboard/', DashboardStatsView.as_view(), name='attendance-dashboard'),
    path('reports/export/', AttendanceReportExportView.as_view(), name='attendance-export'),
]
