from rest_framework import serializers

from accounts.models import User
from .models import School
from utilities.CommonFunctions import validate_pincode, valid_website


class SchoolSerializer(serializers.ModelSerializer):
    school_id = serializers.IntegerField(read_only=True,source="pk")
    class Meta:
        model = School
        fields = ['user', 'name', 'address_line1', 'registration_no', 'board', 'gstin',
                  'phone', 'email', 'owner_phone', 'logo', 'address_line2', 'city', 'pincode', 'state', 'country',
                  'logo', 'principle_name',"school_id"]

    def create(self, validated_data):
        user = User.objects.get(username=validated_data.get('user'))

        school = School(
            phone=validated_data.get('phone'),
            board=validated_data.get('board'),
            address_line1=validated_data.get('address_line1', None),
            name=validated_data.get('name'),
            registration_no=validated_data.get('registration_no'),
            email=validated_data.get('email', None),
            owner_phone=validated_data.get('owner_phone', None),
            website=validated_data.get('website', None),
            address_line2=validated_data.get('address_line2', None),
            city=validated_data.get('city', None),
            pincode=validated_data.get('pincode', None),
            state=validated_data.get('state', None),
            country=validated_data.get('country', None),
            gstin=validated_data.get('gstin', None),
            logo=validated_data.get('logo', None),
            principle_name=validated_data.get("principle_name", None)
        )
        school.user = user
        return school

    def validate_address_line1(self, value):
        if not value:
            raise serializers.ValidationError("can't be empty")
        return value

    def validate_city(self, value):
        if not value:
            raise serializers.ValidationError("can't be empty")
        return value

    def validate_state(self, value):
        if not value:
            raise serializers.ValidationError("can't be empty")
        return value

    def validate_country(self, value):
        if not value:
            raise serializers.ValidationError("can't be empty")
        return value

    def validate_pincode(self, value):
        is_valid = validate_pincode(value)
        if is_valid:
            return value
        raise serializers.ValidationError("Invalid pincode")

    def validate_website(self, value):
        is_valid = valid_website(value)
        if is_valid:
            return value
        raise serializers.ValidationError("Invalid website")

    def validated_email(self, value):
        if not value:
            raise serializers.ValidationError("can't be empty")
        return value

    def validate_school_level(self, value):
        if not value:
            raise serializers.ValidationError("can't be empty")
        return value
