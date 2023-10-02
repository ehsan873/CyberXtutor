from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime
from django.utils.timezone import now


# Create your models here.


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class OTP(models.Model):
    otp = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
