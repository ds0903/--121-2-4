# university_schedule/stats/urls.py
from django.urls import path
from .views import StatsOverview

urlpatterns = [
    path('', StatsOverview.as_view(), name='stats-overview'),
]
