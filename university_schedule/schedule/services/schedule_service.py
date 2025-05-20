from django.db import transaction
from ..models import ScheduleEntry

class ScheduleService:
    @staticmethod
    @transaction.atomic
    def create_entry(data):
        # валідації, бізнес-логіка
        return ScheduleEntry.objects.create(**data)

    @staticmethod
    def list_entries(filters):
        return ScheduleEntry.objects.select_related('group','room','discipline','teacher').filter(**filters)