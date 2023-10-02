import os
import time

from rest_framework import serializers

from .models import Student, CurrentStudent, StudentHistory, StudentCsv
from school.serializer import SchoolSerializer


class StudentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    registration_no = serializers.SerializerMethodField()
    class Meta:
        model = Student
        fields = ['user', 'first_name', 'middle_name', 'last_name', 'gender', 'father_name', 'mother_name', 'phone_no',
                  'email',
                  'parents_no', 'dob', 'address_line1', 'address_line2', 'city', 'state', 'country',
                  'pincode', 'id', "created_at", "username", "created_at","profile_image","registration_no"]

    def get_username(self, obj):
        return obj.user.username

        def create(self, validated_data):
            instance = Student.objects.create(
                user=self.context.get('user', None),
                name=self.context.get('first_name', None),
                email=self.context.get('middle_name', None),
                phone_no=self.context.get('phone_no', None),
                gender=self.context.get('gender', None),
                last_name=self.context.get('last_name', None),
                father_name=self.context.get('father_name', None),
                mother_name=self.context.get('mother_name', None),
                parents_no=self.context.get('parents_no', None),
                dob=self.context.get('dob', None),
                address_line1=self.context.get('address_line1', None),
                address_line2=self.context.get('address_line2', None),
                city=self.context.get('city', None),
                state=self.context.get('state', None),
                country=self.context.get('country', None),
                pincode=self.context.get('pincode', None),

            )

            return instance
    def get_registration_no(self,obj):
            return CurrentStudent.objects.get(student=obj).registration_no


    def update(self, instance, validated_data):
        # Update the fields in the instance with the validated data

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.father_name = validated_data.get('father_name', instance.father_name)
        instance.mother_name = validated_data.get('mother_name', instance.mother_name)
        instance.email = validated_data.get('email', instance.email)
        # instance.registartion_no = validated_data.get('registartion_no', instance.registartion_no)
        instance.country = validated_data.get('country', instance.country)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.parents_no = validated_data.get('parents_no', instance.parents_no)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.city = str(validated_data.get('city', instance.city))
        instance.state = validated_data.get('state', instance.state)
        instance.country = validated_data.get('country', instance.country)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.address_line1 = validated_data.get('address_line1', instance.address_line1)
        instance.address_line2 = validated_data.get('address_line2', instance.address_line2)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)

        instance.save()
        return instance


class CurrentStudentSerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(many=False, source='student')
    class_name = serializers.CharField(source='school_class.name')
    class_name_id = serializers.CharField(source='school_class.pk')
    section = serializers.CharField(source="section.section")
    section_id = serializers.CharField(source="section.pk")
    session = serializers.CharField(source="session.name")
    profile_image = serializers.CharField(source="student.profile_image")
    school_details = serializers.SerializerMethodField()
    change_session_id = serializers.CharField(source='student.pk')

    class Meta:
        model = CurrentStudent
        fields = ['id', 'student_details', 'class_name', 'section', 'session', 'registration_no', 'profile_image',
                  'school_details', 'change_session_id', 'class_name_id', 'section_id']

    def get_school_details(self, obj):
        serialzer = SchoolSerializer(obj.school, many=False)
        return serialzer.data


class StudentHistorySerializer(serializers.ModelSerializer):
    student_details = StudentSerializer(many=False, source='student')
    class_name = serializers.CharField(source='school_class.name')
    section = serializers.CharField(source="section.section")
    session = serializers.CharField(source="session.name")
    profile_image = serializers.CharField(source="student.profile_image")
    school_details = serializers.SerializerMethodField()
    change_session_id = serializers.CharField(source='student.pk')

    class Meta:
        model = StudentHistory
        fields = ['id', 'student_details', 'class_name', 'section', 'session', 'registration_no', 'profile_image',
                  'school_details', 'change_session_id']

    def get_school_details(self, obj):
        serialzer = SchoolSerializer(obj.school, many=False)
        return serialzer.data


class CurrentStudentResultSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source="student.id", read_only=True)
    student_name = serializers.SerializerMethodField()

    class Meta:
        model = CurrentStudent
        fields = ['student_id', "student_name"]

    def get_student_name(self, obj):
        name = obj.student.first_name
        if obj.student.middle_name:
            name = name + " " + obj.student.middle_name
        if obj.student.last_name:
            name = name + " " + obj.student.last_name
        return name


class StudentCsvSerializer(serializers.ModelSerializer):
    csv_id = serializers.CharField(source="id")
    session = serializers.CharField(source="session.name")
    file_name = serializers.SerializerMethodField()
    class Meta:
        model = StudentCsv
        fields = ['csv', 'created_at', 'csv_id', "session","file_name"]

    def get_file_name(self, obj):
        return os.path.basename(obj.csv.name)
