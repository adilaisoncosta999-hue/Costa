from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, DepartmentViewSet, PositionViewSet, WorkScheduleViewSet

router = DefaultRouter()
router.register('companies', CompanyViewSet, basename='company')
router.register('departments', DepartmentViewSet, basename='department')
router.register('positions', PositionViewSet, basename='position')
router.register('schedules', WorkScheduleViewSet, basename='schedule')

urlpatterns = router.urls
