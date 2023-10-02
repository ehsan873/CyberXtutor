import re

from django.db import models
from rest_framework.exceptions import ValidationError

from school.models import School


# Create your models here.
def validate_name(value):
    # Perform your validation logic here
    pattern = r'^\d{4}-\d{2}$'
    if not re.match(pattern, value):
        raise ValidationError("Invalid format for my_field. Expected format: YYYY-YY.")


class Session(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False, validators=[validate_name])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
