from django.db import models

# Create your models here.
from django.db import models

from accounts.models import User


# Create your models here.
class School(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_no = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    email = models.CharField(max_length=200, null=False, blank=False)
    phone = models.CharField(max_length=200, null=False, blank=False)
    owner_phone = models.CharField(max_length=200, null=False, blank=False)
    logo = models.ImageField(max_length=200, null=True, blank=True, upload_to="school_logo/")
    gstin = models.CharField(max_length=200, null=True, blank=True)
    website = models.CharField(max_length=200, null=True, blank=True)
    board = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    address_line1 = models.CharField(max_length=200, null=False, blank=False, )
    address_line2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=False, blank=False)
    state = models.CharField(max_length=200, null=False, blank=False, )
    country = models.CharField(max_length=200, null=False, blank=False, )
    pincode = models.CharField(max_length=10, null=False, blank=False)
    school_level = models.CharField(max_length=100, null=False, blank=False),
    principle_name = models.CharField(max_length=300, default="", null=False, blank=False)
