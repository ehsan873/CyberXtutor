from django.db import models

from school.models import School

from session.models import Session


# Create your models here.
class SchoolClass(models.Model):
    name = models.CharField(max_length=60, null=False, blank=False)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ClassSection(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    section = models.CharField(max_length=60, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CurrentClassSection(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, related_name="sectionname")
    schoolclass = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name="classname")
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
