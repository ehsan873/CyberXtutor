import time

from django.middleware import csrf
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from utilities.permissions import IsAdmin, IsSchool, IsStudent, IsSchoolOrStudent
from rest_framework.response import Response
from rest_framework.views import APIView
import logging

from utilities.CommonFunctions import sort_class

log = logging.getLogger(__name__)
from school.models import School

from .models import SchoolClass, ClassSection, CurrentClassSection
# from session.models import SchoolSession
# from .models import SchoolClass, ClassSection
from .serializer import ClassSectionSerializer, SchoolClassSerilizer, CurrentClassSectionSerializer
from session.models import Session


# Create your views here.
@method_decorator(csrf_exempt, name='post')
class ClassView(APIView):
    # Set the required permission classes
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request):
        # Retrieve the school associated with the user
        school = School.objects.get(user=request.user)
        # Get the class sections and classes belonging to the school
        classes_sections = ClassSection.objects.filter(school=school)
        classes = SchoolClass.objects.filter(school=school)
        # Serialize the class sections and classes
        section_serializer = ClassSectionSerializer(classes_sections, many=True)
        classes_serializer = SchoolClassSerilizer(classes, many=True)
        # Return the serialized data in the response
        return Response({"Success": True,
                         "Data": {'sections': section_serializer.data,
                                  'classes': classes_serializer.data
                                  }}, status=status.HTTP_201_CREATED)

    def post(self, request):
        # Get the classes data from the request
        classes = request.data
        # Get the school associated with the user
        school = School.objects.get(user=request.user)
        # Retrieve the classes already added for the school
        already_added_class = SchoolClass.objects.filter(school=school)
        # Initialize variables
        list_of_class = []
        errors = []
        error = False
        # Check if there are classes to add
        if len(classes) == 0:
            error = True
            errors.append("No class to add")

        try:
            # Iterate through each class in the request data
            for cls in classes:
                if not cls['name']:
                    error = True
                    errors.append("class name reqired")
                elif already_added_class.filter(name=cls['name']).exists():
                    error = True
                    errors.append("class already added " + cls['name'])
                else:
                    # Create a SchoolClass instance and add it to the list
                    list_of_class.append(SchoolClass(name=cls['name'], school=school))
        except Exception as e:
            log.error("Error from ClassView's Post" + str(e))
            return Response({"Success": False,
                             "Data": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        # Check if there were any errors during processing
        if error:
            return Response({"Success": False,
                             "Data": errors}, status=status.HTTP_400_BAD_REQUEST)
        SchoolClass.objects.bulk_create(list_of_class)
        return Response({"Success": True,
                         "Data": ["Class created"]}, status=status.HTTP_201_CREATED)


class SectionView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def post(self, request):
        sections = request.data
        school = School.objects.get(user=request.user)
        already_added_section = ClassSection.objects.filter(school=school)
        list_of_section = []
        errors = []
        error = False
        if not isinstance(request.data, list):
            error = True
            errors.append("No section to add")
        if len(sections) < 1:
            error = True
            errors.append("No section to add")
        try:
            for section in sections:
                if not section['section']:
                    error = True
                    errors.append("section required")
                elif already_added_section.filter(section=section['section']).exists():
                    error = True
                    errors.append("Section already added " + section['section'])
                else:
                    list_of_section.append(
                        ClassSection(section=section['section'],
                                     school=school
                                     )
                    )
        except Exception as e:
            log.error("Error from SectionView's get" + str(e))
            if error:
                return Response({"Success": False,
                                 "Data": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        if error:
            return Response({"Success": False,
                             "Data": errors}, status=status.HTTP_400_BAD_REQUEST)
        ClassSection.objects.bulk_create(list_of_section)
        return Response({"Success": True,
                         "Data": ["Section created"]}, status=status.HTTP_201_CREATED)


class ClassSectionByIdView(APIView):

    def patch(self, request, class_section_id):
        school = School.objects.get(user=request.user)
        section = request.data.get("section", None)
        if not section:
            return Response({"Success": False,
                             "Data": ["Section can't be empty"]}, status=status.HTTP_400_BAD_REQUEST)
        # if not ClassSection.objects.filter(pk=class_section_id).exists():
        #     return Response({"Success": False,
        #                      "Data": ["Invalid session classes id"]}, status=status.HTTP_400_BAD_REQUEST)
        # class_section = ClassSection.objects.get(pk=class_section_id)
        # if school.registration_no != class_section.session.school.registration_no:
        #     return Response({"Success": False,
        #                      "Data": ["Invalid session classes id"]}, status=status.HTTP_400_BAD_REQUEST)
        #
        # class_section.section = section
        # class_section.save()
        #
        # return Response({"Success": True,
        #                  "Data": ["Class updated"]}, status=status.HTTP_202_ACCEPTED)


class CurrentClass(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request, *args, **kwargs):
        # Get the school associated with the user
        school = School.objects.get(user=request.user)

        # Retrieve the current classes for the school
        current_classes = CurrentClassSection.objects.filter(school=school)
        # Get the session ID from the request parameters
        session_id = request.GET.get('session_id', None)
        class_id = request.GET.get('class_id', None)
        section_id = request.GET.get('section_id', None)
        if not session_id:
            # If no session ID provided, retrieve all sessions
            session = Session.objects.all()
        else:
            # If session ID provided, filter sessions by ID
            session = Session.objects.filter(pk=session_id)
            # Check if the specified session exists
            if not session.exists():
                return Response({"Success": False,
                                 "Data": "invalid session"}, status=status.HTTP_400_BAD_REQUEST)
        # Filter the current classes by the specified sessions and school
        current_classes = CurrentClassSection.objects.prefetch_related('section', 'schoolclass').filter(
            session__in=session, school=school)
        if class_id and SchoolClass.objects.filter(pk=class_id).exists():
            current_classes = current_classes.filter(schoolclass=SchoolClass.objects.get(pk=class_id))
        if section_id and ClassSection.objects.filter(pk=section_id).exists():
            current_classes = current_classes.filter(section=ClassSection.objects.get(pk=section_id))
        serializer = CurrentClassSectionSerializer(current_classes, many=True)
        class_data = sort_class(serializer.data)
        return Response({"Success": True,
                         "Data": class_data}, status=status.HTTP_202_ACCEPTED)

    def post(self, request):
        try:
            data = request.data[0]

        except Exception as e:
            log.error("Error from CurrentClass's Post" + str(e))
            return Response({"Success": False,
                             "Data": "invalid format"}, status=status.HTTP_400_BAD_REQUEST)
        school = School.objects.get(user=request.user)
        schoolsections = ClassSection.objects.filter(school=school)
        schoolclasses = SchoolClass.objects.filter(school=school)
        # current_classes = CurrentClassSection.objects.filter(school=school)
        # print(data)
        try:
            session_id = data.get('session_id', None)
        except Exception as e:
            log.error("Error from ClassView's Post" + str(e))
            return Response({"Success": False,
                             "Data": "invalid format"}, status=status.HTTP_400_BAD_REQUEST)

        session = Session.objects.filter(pk=session_id)

        if not session_id or not session.exists():
            return Response({"Success": False,
                             "Data": "invalid session id"}, status=status.HTTP_400_BAD_REQUEST)
        current_classes = CurrentClassSection.objects.filter(school=school, session=session[0])
        if not session_id or not session.exists():
            return Response({"Success": False,
                             "Data": "invalid session id"}, status=status.HTTP_400_BAD_REQUEST)
        class_data = data.get("classes")
        errors = []
        error = False
        if not isinstance(class_data, list):
            error = True
            errors.append("No class to add")
        if len(class_data) < 1:
            error = True
            errors.append("No class to add")
        if error:
            return Response({"Success": False,
                             "Data": errors}, status=status.HTTP_400_BAD_REQUEST)

        list_of_classes = []
        for classes in class_data:
            classname = classes.get('class_name').lower()
            sectionname = classes.get('section_name').lower()
            if not classname or not sectionname:
                errors.append("class_name and section_name can't be empty ")
                error = True
                break
            else:
                if schoolclasses.filter(name=classname).exists():
                    school_class = schoolclasses.get(name=classname)
                else:
                    school_class = SchoolClass.objects.create(name=classname, school=school)
                if schoolsections.filter(section=sectionname).exists():
                    classsection = schoolsections.get(section=sectionname)
                else:
                    classsection = ClassSection.objects.create(section=sectionname, school=school)
                # school_class = SchoolClass.objects.get_or_create(, school=school)
                # classsection = ClassSection.objects.get_or_create(section=sectionname, school=school)
                if current_classes.filter(
                        school=school,
                        section=classsection,
                        schoolclass=school_class,
                        session=session[0]
                ).exists():
                    errors.append("class_name " + classname + "  and section_name  " + sectionname + " already exists")
                    error = True
                    break
                list_of_classes.append(
                    CurrentClassSection(
                        school=school,
                        section=classsection,
                        schoolclass=school_class,
                        session=session[0]
                    )
                )
        if error:
            return Response({"Success": False,
                             "Data": errors}, status=status.HTTP_400_BAD_REQUEST)
        CurrentClassSection.objects.bulk_create(list_of_classes)
        return Response({"Success": True,
                         "Data": "Classes created"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        class_id = request.data.get('class_id', None)
        school = School.objects.get(user=request.user)
        if not CurrentClassSection.object.filter(pk=class_id, school=school).exists():
            return Response({"Success": False,
                             "Data": "Invalid class id"}, status=status.HTTP_400_BAD_REQUEST)

        CurrentClassSection.object.get(pk=class_id, school=school).delete()
        if not CurrentClassSection.object.filter(pk=class_id, school=school).exists():
            return Response({"Success": True,
                             "Data": "Class deleted"}, status=status.HTTP_202_ACCEPTED)


class UpdateClassSectionView(APIView):

    def patch(self, request, class_section_id):
        school = School.objects.get(user=request.user)

        session_id = request.data.get('session_id', None)
        sectionname = request.data.get('section_name', None)
        classname = request.data.get('class_name', None)
        new_seesion = request.data.get('new_session_id', None)
        if not session_id or not Session.objects.filter(pk=session_id).exists():
            return Response({"Success": False,
                             "Data": "Invalid session  id"}, status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.get(pk=session_id)
        if not CurrentClassSection.objects.filter(pk=class_section_id, school=school, session=session).exists():
            return Response({"Success": False,
                             "Data": "Invalid class and section id"}, status=status.HTTP_400_BAD_REQUEST)
        current_class_secton = CurrentClassSection.objects.get(pk=class_section_id, school=school, session=session)
        if sectionname:
            if current_class_secton.section.section != sectionname:
                if ClassSection.objects.filter(section__iexact=sectionname, school=school).exists():
                    current_class_secton.section = ClassSection.objects.get(section__iexact=sectionname, school=school)
                else:
                    current_class_secton.section = ClassSection.objects.create(section=sectionname, school=school)

        if classname:
            if current_class_secton.schoolclass.name != classname:
                if SchoolClass.objects.filter(name__iexact=classname, school=school).exists():
                    current_class_secton.schoolclass = SchoolClass.objects.get(name__iexact=classname, school=school)
                else:
                    current_class_secton.schoolclass = SchoolClass.objects.create(name=classname, school=school)
        # print(current_class_secton)
        # print(current_class_secton.section.section)
        if CurrentClassSection.objects.filter(section=current_class_secton.section,
                                              schoolclass=current_class_secton.schoolclass).exists():
            return Response({"Success": False,
                             "Data": "Class already exist "}, status=status.HTTP_400_BAD_REQUEST)
        if new_seesion and Session.objects.filter(pk=new_seesion).exists():
            session = Session.objects.ge(pk=session_id)
            current_class_secton.session = session
        current_class_secton.save()

        return Response({"Success": True,
                         "Data": "Class updated"}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, class_section_id):
        school = School.objects.get(user=request.user)

        session_id = request.data.get('session_id', None)
        if not session_id or not Session.objects.filter(pk=session_id).exists():
            return Response({"Success": False,
                             "Data": "Invalid session  id"}, status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.get(pk=session_id)
        # print(CurrentClassSection.objects.filter(pk=class_section_id, school=school, session=session))
        if not CurrentClassSection.objects.filter(pk=class_section_id, school=school, session=session).exists():
            print(class_section_id)
            return Response({"Success": False,
                             "Data": "Invalid class and section id"}, status=status.HTTP_400_BAD_REQUEST)
        current_class_secton = CurrentClassSection.objects.get(pk=class_section_id, school=school, session=session)
        current_class_secton.delete()
        return Response({"Success": True,
                         "Data": "class delete"}, status=status.HTTP_202_ACCEPTED)


def get_class_and_section(session,school):
    current_classes = CurrentClassSection.objects.prefetch_related('section', 'schoolclass').filter(
        session__in=session, school=school)
    serializer = CurrentClassSectionSerializer(current_classes, many=True)
    class_data = sort_class(serializer.data)
    return Response({"Success": True,
                     "Data": class_data}, status=status.HTTP_202_ACCEPTED)


class AdminClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get the school associated with the user
        school_id = request.GET.get("school_id",None)
        try:
            school = School.objects.get(pk=school_id)
        except Exception as e:
            return Response({"Success": False,
                             "Data": "Inavalid school id"}, status=status.HTTP_400_BAD_REQUEST)
        # Retrieve the current classes for the school
        current_classes = CurrentClassSection.objects.filter(school=school)
        # Get the session ID from the request parameters
        session_id = request.GET.get('session_id', None)
        if not session_id:
            # If no session ID provided, retrieve all sessions
            session = Session.objects.all()
        else:
            # If session ID provided, filter sessions by ID
            session = Session.objects.filter(pk=session_id)
            # Check if the specified session exists
            if not session.exists():
                return Response({"Success": False,
                                 "Data": "invalid session"}, status=status.HTTP_400_BAD_REQUEST)
        # Filter the current classes by the specified sessions and school
        return get_class_and_section(session,school)
