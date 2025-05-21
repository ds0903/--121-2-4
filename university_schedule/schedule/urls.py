from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
     RoomViewSet, DisciplineViewSet,
    GroupViewSet, TeacherViewSet, ScheduleEntryViewSet
)

router = DefaultRouter()
router.register('rooms',       RoomViewSet)
router.register('disciplines', DisciplineViewSet)
router.register('groups',      GroupViewSet)
router.register('teachers',    TeacherViewSet)
router.register('schedule', ScheduleEntryViewSet, basename='scheduleentry')
urlpatterns = [
    path('', include(router.urls)),
]
