import time

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'is_school', 'is_student', 'is_teacher']

    def create(self, validated_data):
        is_school = self.context.get('is_school', False)
        is_student = self.context.get('is_student', False)
        is_teacher = self.context.get('is_teacher', False)
        # print(self.context.get('username'))
        # time.sleep(100)
        user = User(username=self.context.get('username'))
        if is_school:
            user.is_school = True
        elif is_student:
            user.is_student = True
        elif is_teacher:
            user.is_teacher = True
        user.set_password(validated_data.get('password'))
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    role = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs['role'] = ""
        data = super().validate(attrs)
        if self.user.is_school:
            role = "school"
        elif self.user.is_student:
            role = "student"
        elif self.user.is_teacher:
            role = "teacher"
        else:
            role = "admin"
        data['role'] = role
        return data
