from django.db import models

from accounts.models import User
from classes.models import SchoolClass, ClassSection

from school.models import School
from session.models import Session


# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/', null=True, blank=True)
    first_name = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=200, blank=False, null=False)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=False, null=False)
    phone_no = models.CharField(max_length=200, blank=True, null=True)
    parents_no = models.CharField(max_length=200, blank=True, null=True)
    dob = models.CharField(max_length=200, null=False, blank=False, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    city = models.CharField(max_length=200, null=False, blank=False, )
    state = models.CharField(max_length=200, null=False, blank=False, )
    country = models.CharField(max_length=200, null=False, blank=False, )
    pincode = models.CharField(max_length=200, null=False, blank=False, )

    # related to school
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, null=True)

    registration_no = models.CharField(max_length=40, blank=False, null=False)

    class Meta:
        unique_together = ('school', 'registration_no',)


class StudentHistory(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True)
    school_class = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, null=True)
    class_section = models.ForeignKey(ClassSection, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    registration_no = models.CharField(max_length=40, blank=False, null=False)

    class Meta:
        unique_together = ('school', 'registration_no', 'session')
