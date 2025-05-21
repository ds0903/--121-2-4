# university_schedule/core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Teacher, Room, Discipline, Group

User = get_user_model()

class TeacherSerializer(serializers.ModelSerializer):
    # Обов’язкове поле для запису юзера-профілю, write-only
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.exclude(role='student'),
        source='user',
        write_only=True,
        help_text="ID існуючого CustomUser, який не має role='student'"
    )
    # Для читання віддаємо вже вкладений user.username
    user = serializers.CharField(
        source='user.username',
        read_only=True
    )

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'user_id', 'disciplines']

    def validate_user(self, value):
        # Ця валідація переписуєте для source='user'
        if getattr(value, 'role', None) == 'student':
            raise serializers.ValidationError("Студент не може бути викладачем")
        return value
