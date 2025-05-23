import pytest
from university_schedule.schedule.models import ScheduleEntry
from university_schedule.core.models import Room, Discipline, Teacher

@pytest.mark.django_db
def test_editor_can_create_entry(auth_client, group, create_user):
    client, editor = auth_client("ed1", "editor")
    # створюємо залежності
    room = Room.objects.create(name="R1")
    disc = Discipline.objects.create(title="D1")
    user_teacher = create_user("t1", "teacher")
    teacher = Teacher.objects.create(user=user_teacher)
    # POST розкладу
    resp = client.post("/api/schedule/schedule/", {
        "group_id": group.id,
        "room_id": room.id,
        "discipline_id": disc.id,
        "teacher_id": teacher.id,
        "start_time": "2025-06-01T09:00:00Z",
        "end_time":   "2025-06-01T10:00:00Z",
        "weekday": "Monday"
    }, format="json")
    assert resp.status_code == 201
    assert ScheduleEntry.objects.count() == 1

@pytest.mark.django_db
def test_student_cannot_create(auth_client, group, create_user):
    client, student = auth_client("s1", "student")
    resp = client.post("/api/schedule/schedule/", {})
    assert resp.status_code == 403

@pytest.mark.django_db
def test_teacher_sees_only_their_entries(auth_client, group, create_user):
    client, teacher_user = auth_client("t2", "teacher")
    room = Room.objects.create(name="R2")
    disc = Discipline.objects.create(title="D2")
    teacher = Teacher.objects.create(user=teacher_user)
    # створимо два записи: один на цього вчителя, інший на іншого
    ScheduleEntry.objects.create(
        group=group, room=room, discipline=disc,
        teacher=teacher, start_time="2025-06-01T09:00Z",
        end_time="2025-06-01T10:00Z", weekday="Monday"
    )
    other_user = create_user("t3", "teacher")
    other_teacher = Teacher.objects.create(user=other_user)
    ScheduleEntry.objects.create(
        group=group, room=room, discipline=disc,
        teacher=other_teacher, start_time="2025-06-01T11:00Z",
        end_time="2025-06-01T12:00Z", weekday="Monday"
    )
    resp = client.get("/api/schedule/schedule/")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["teacher"] == teacher_user.username
