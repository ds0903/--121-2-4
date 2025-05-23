import pytest
from university_schedule.schedule.models import ScheduleEntry
from university_schedule.core.models import Room, Discipline, Teacher
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_manager_sees_stats(auth_client, group, create_user):
    client, manager = auth_client("m1", "manager")
    # підготуємо дані
    room = Room.objects.create(name="R3")
    disc = Discipline.objects.create(title="D3")
    user_t = create_user("t4", "teacher")
    teacher = Teacher.objects.create(user=user_t)
    ScheduleEntry.objects.create(
        group=group, room=room, discipline=disc,
        teacher=teacher, start_time="2025-06-02T09:00Z",
        end_time="2025-06-02T10:00Z", weekday="Tuesday"
    )
    resp = client.get("/api/stats/")
    assert resp.status_code == 200
    body = resp.json()
    assert "lessons_per_room" in body
    assert body["lessons_per_room"][0]["room__name"] == "R3"

@pytest.mark.django_db
def test_editor_cannot_see_stats(auth_client):
    client, editor = auth_client("e2", "editor")
    resp = client.get("/api/stats/")
    assert resp.status_code == 403
