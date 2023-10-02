from rest_framework import serializers

from .models import ClassSection, SchoolClass, CurrentClassSection


class ClassSectionSerializer(serializers.ModelSerializer):
    # class_name = serializers.CharField(source='school_class.name')

    class Meta:
        model = ClassSection
        fields = ['id', 'section']


class SchoolClassSerilizer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['id', 'name']


class CurrentClassSectionSerializer(serializers.ModelSerializer):
    class_name = serializers.CharField(source="schoolclass.name")
    section_name = serializers.CharField(source="section.section")
    class_id = serializers.CharField(source="schoolclass.id")
    section_id = serializers.CharField(source="section.id")
    session_name = serializers.CharField(source="session.name")
    session_id = serializers.CharField(source="session.id")
    class Meta:
        model = CurrentClassSection
        fields = ['id', 'class_name', 'section_name', "class_id", "section_id","session_name","session_id"]
