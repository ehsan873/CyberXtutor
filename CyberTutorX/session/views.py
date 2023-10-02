from operator import itemgetter

from django.contrib.sessions.backends import file
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.views import APIView
from utilities.permissions import IsAdmin, IsSchool
from utilities.SessionHelper import is_valid_session

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from school.models import School

from .models import Session
from utilities.CSVHelper import convert_to_xlsx, get_file_path

from .serializer import SessionSerializer
from utilities.email import get_email_template


# Create your views here.
class AddSessionView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        # school = School.objects.get(user=request.user)
        # csv_file = request.data.get('csv')
        # file_path = get_file_path(csv_file)
        session_text = request.data.get("session", None)
        # is_current_session = request.data.get("is_current", False)

        if not session_text or not is_valid_session(session_text) or not isinstance(session_text,str):
            return Response({
                "Success": False,
                'data': [{'Error': 'Please provide valid session'}]},
                status=status.HTTP_400_BAD_REQUEST)
        if Session.objects.filter(name=session_text).exists():
            return Response({
                "Success": False,
                'data': [{'Error': 'Session already exists'}]},
                status=status.HTTP_400_BAD_REQUEST)
        session_object = Session.objects.create(name=session_text)
        return Response({
            "Success": True,
            'data': [{'Error': 'Session created'}]},
            status=status.HTTP_201_CREATED)


class GetAllSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # school = School.objects.get(user=request.user)
        sesion_query = Session.objects.all()
        session_serializer = SessionSerializer(sesion_query, many=True)

        return Response({
            "Success": True,
            'data': sorted(session_serializer.data, key=itemgetter('name'), reverse=True)},
            status=status.HTTP_202_ACCEPTED)



# classes SessionView(APIView):
#     permission_classes = [IsAuthenticated, IsSchool]
#
#     def get(self, request, school_session):


