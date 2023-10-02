import time
import logging

log = logging.getLogger(__name__)
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# from utilities.permissions import IsStudent

from utilities.permissions import IsSchool

from .models import School
from .serializer import SchoolSerializer


# Create your views here.
class SchoolView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request):
        school = School.objects.get(user=request.user)
        serializer = SchoolSerializer(school, many=False)
        return Response({"Success": True,
                         "Data": serializer.data}, status=status.HTTP_201_CREATED)

    def patch(self, request):
        image = request.data.get('image')
        school = School.objects.get(user=request.user)
        if not image:
            return Response({"Success": False,
                             "Data": ['image cant be empty']}, status=status.HTTP_400_BAD_REQUEST)
        school.logo = image
        school.save()
        return Response({"Success": True,
                         "Data": ['image uploaded']}, status=status.HTTP_202_ACCEPTED)
        # time.sleep(100)


class UpdateSchoolView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def patch(self, request):
        user = request.user
        school = School.objects.get(user=request.user)
        serializer = SchoolSerializer(instance=school, data=request.data, partial=True)
        if serializer.is_valid():
            school = serializer.save()
            try:
                school.save()
            except Exception as e :
                error =e
            return Response({"Success": True,
                             "Data": ['updated']}, status=status.HTTP_202_ACCEPTED)
        return Response({"Success": False,
                         "Data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AdminSchooView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        school = School.objects.all()
        serializer = SchoolSerializer(school,many=True)
        return Response({"Success": True,
                         "Data": serializer.data}, status=status.HTTP_200_OK)