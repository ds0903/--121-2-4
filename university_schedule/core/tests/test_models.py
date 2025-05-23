import pytest
from university_schedule.core.models import Group, Room, Discipline, Teacher
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_group_str():
    g = Group.objects.create(name="G1")
    assert str(g) == "G1"

@pytest.mark.django_db
def test_teacher_user_link(create_user):
    user = create_user("teach1", "teacher")
    d1 = Discipline.objects.create(title="Math")
    t = Teacher.objects.create(user=user)
    t.disciplines.add(d1)
    assert t.user.username == "teach1"
    assert d1 in t.disciplines.all()
