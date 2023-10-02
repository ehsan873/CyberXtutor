import re

from rest_framework import serializers

from .models import Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'name']

    def validate_name(self, value):
        pattern = r'^\d{4}-\d{2}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid format for my_field. Expected format: YYYY-YY.")

        return value
