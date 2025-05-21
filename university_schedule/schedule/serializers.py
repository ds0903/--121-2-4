from rest_framework import serializers
from .models import ScheduleEntry

from rest_framework import serializers
from .models import Room, Discipline, Group, Teacher

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'title']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'users']

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name']


class ScheduleEntrySerializer(serializers.ModelSerializer):
    room       = RoomSerializer(read_only=True)
    room_id    = serializers.PrimaryKeyRelatedField(
                      queryset=Room.objects.all(),
                      source='room',
                      write_only=True
                  )
    group      = GroupSerializer(read_only=True)
    group_id   = serializers.PrimaryKeyRelatedField(
                      queryset=Group.objects.all(),
                      source='group',
                      write_only=True
                  )
    discipline = DisciplineSerializer(read_only=True)
    discipline_id = serializers.PrimaryKeyRelatedField(
                        queryset=Discipline.objects.all(),
                        source='discipline',
                        write_only=True
                    )
    teacher    = serializers.CharField(source='teacher.user.username', read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
                      queryset=Teacher.objects.all(),
                      source='teacher',
                      write_only=True
                  )

    class Meta:
        model = ScheduleEntry
        fields = [
          'id',
          'room', 'room_id',
          'group','group_id',
          'discipline','discipline_id',
          'teacher','teacher_id',
          'start_time','end_time','weekday',
        ]

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError({
                'end_time': 'end_time must be after start_time'
            })
        return data