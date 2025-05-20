from rest_framework.routers import DefaultRouter
from .views import ScheduleEntryViewSet

router = DefaultRouter()
router.register(r'schedule', ScheduleEntryViewSet)
urlpatterns = router.urls