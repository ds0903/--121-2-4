# university_schedule/core/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Teacher, Room, Discipline, Group

User = get_user_model()

class TeacherSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.exclude(role='student'),
        source='user',
        write_only=True,
        help_text="ID існуючого CustomUser, який не має role='student'"
    )
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'name', 'user', 'user_id']

    def validate_user_id(self, value):
        if getattr(value, 'role', None) == 'student':
            raise serializers.ValidationError("Студент не може бути викладачем")
        return value

    def create(self, validated_data):
        user = validated_data.get('user')
        # Якщо для цього user вже є Teacher — кидаємо зрозумілу помилку
        if Teacher.objects.filter(user=user).exists():
            raise serializers.ValidationError({
                'user_id': 'Профіль викладача для цього користувача вже створено.'
            })
        return super().create(validated_data)
