from django.db import models

from classes.models import SchoolClass, ClassSection
from school.models import School


# Create your models here.

class Subject(models.Model):
    name = models.TextField(max_length=50, blank=False, null=False)
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass,on_delete=models.CASCADE)
    class_section = models.ForeignKey(ClassSection,on_delete=models.CASCADE)

