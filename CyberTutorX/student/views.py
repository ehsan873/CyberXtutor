import copy
import multiprocessing
import time
from datetime import datetime
from django.db import connection, transaction

import pandas as pd
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, Subquery
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from utilities.CommonFunctions import sort_sessions_by_name
from utilities.permissions import IsSchool
import logging

from utilities.permissions import IsStudent

log = logging.getLogger(__name__)
from school.models import School



from classes.models import SchoolClass, ClassSection
from session.models import Session
from .models import Student, StudentHistory
from .serializer import StudentSerializer, CurrentStudentSerializer, StudentHistorySerializer, StudentCsvSerializer
from accounts.models import User

from utilities.ResultExcelGenerator import ResultExcelGenerator

from utilities.SchoolExcelGenerator import SchoolExcelGenerator

from utilities.SchoolExcelValidator import SchoolExcelValidator

from utilities.AccountHelper import generate_random_password

from classes.models import CurrentClassSection

from utilities.CredentialExcelGenerator import CredentialExcelGenerator



fs = FileSystemStorage(location='excel/')


class StudentPagination(PageNumberPagination):
    page_size = 10000000000000000000  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100000000000000000  # Maximum number of items per page


# Create your views here.
def has_every_field(data):
    error = []
    if not data.get("phone_no"):
        error.append("Phone no is required field")
    if not data.get('gender'):
        error.append("gender no is required field")
    if not data.get('first_name'):
        error.append("First name is required")
    if not data.get('mother_name'):
        error.append("Mother name is required")
    if not data.get("registration_no"):
        error.append("Registration no is required")
    if not data.get("father_name"):
        error.append("Father name is is required")
    return error


class SchoolStudentView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]
    pagination_class = StudentPagination

    def get(self, request):
        school = School.objects.get(user=request.user)
        session_id = request.GET.get('session_id', None)
        class_id = request.GET.get('class_id', None)
        section_id = request.GET.get('section_id', None)
        page_size = request.GET.get('limit', None)
        search_term = request.GET.get('search', None)
        students = Student.objects.filter(school=school)
        if session_id and Session.objects.get(pk=session_id).exists():
            students = students.filter(session__id=session_id)
        if class_id and SchoolClass.objects.get(pk=class_id).exists():
            students = students.filter(school_class__id=session_id)
        if section_id and ClassSection.objects.get(pk=section_id).exists():
            students = students.filter(class_section__id=section_id)

        return paginator.get_paginated_response(serialized_data.data)

    def post(self, request):

        school = School.objects.get(user=request.user)
        request_data = request.data.copy()
        if len(has_every_field(request_data)) > 0:
            # print(len(has_every_field(has_every_field())))
            return Response({"Success": False,
                             "Data": has_every_field(request.data)}, status=status.HTTP_400_BAD_REQUEST)

        class_id = request_data.get('class_id', None)
        section_id = request.data.get('section_id', None)
        session_id = request.data.get('session_id', None)
        if not Session.objects.filter(pk=session_id).exists():
            return Response({"Success": False,
                             "Data": ["Invalid session"]}, status=status.HTTP_400_BAD_REQUEST)
        if not SchoolClass.objects.filter(school=school, pk=class_id).exists():
            return Response({"Success": False,
                             "Data": ["Invalid class"]}, status=status.HTTP_400_BAD_REQUEST)
        if not ClassSection.objects.filter(pk=section_id, school=school).exists():
            return Response({"Success": False,
                             "Data": ["Invalid section"]}, status=status.HTTP_400_BAD_REQUEST)
        session = Session.objects.get(pk=session_id)
        school_class = SchoolClass.objects.get(school=school, pk=class_id)
        section = ClassSection.objects.get(pk=section_id, school=school)
        cursor = connection.cursor()
        cursor.execute("select nextval('student_student_id_seq')")
        result = cursor.fetchone()
        username = request_data.get('registration_no') + str(result[0])
        request_data['username'] = username
        password = 123456789
        if request.data.get("password", None):
            password = request.data.get("password")
        user = create_user(request_data, {'username': username, 'is_student': True, 'password': password})
        if not user.get('is_valid'):
            return Response({"Success": False,
                             "Data": user.get('error')}, status=status.HTTP_400_BAD_REQUEST)

        request_data['user'] = user.get('user').pk
        serializer = StudentSerializer(data=request_data, context=request.data | {'user': user.get('user')})

        if serializer.is_valid():
            # print(serializer.validated_data)
            # time.sleep(10)
            student = serializer.save()
            CurrentStudent.objects.create(student=student, school=school, school_class=school_class, session=session,
                                          section=section, registration_no=request_data.get('registration_no'))
            return Response({"Success": True,
                             "Data": ["student created"]}, status=status.HTTP_201_CREATED)
        else:
            return Response({"Success": False,
                             "Data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def valid_student_update_request(data):
    is_valid = True
    error = []
    if data.__contains__("gender"):
        is_valid = False
        error.append("school can't change gender")
    if data.__contains__("email"):
        is_valid = False
        error.append("school can't change email")
    if data.__contains__("parents_no"):
        is_valid = False
        error.append("school can't change parents_no")
    if data.__contains__("father_name"):
        is_valid = False
        error.append("school can't change father_name")
    if data.__contains__("mother_name"):
        is_valid = False
        error.append("school can't change mother_name")
    if data.__contains__("city"):
        is_valid = False
        error.append("school can't change city")
    if data.__contains__("state"):
        is_valid = False
        error.append("school can't change state")
    if data.__contains__("country"):
        is_valid = False
        error.append("school can't change country")
    if data.__contains__("pincode"):
        is_valid = False
        error.append("school can't change pincode")
    return is_valid, error


class SchoolStudentByIdView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request, current_student_id):
        school = School.objects.get(user=request.user)
        student_id = request.GET.get('change_session_id', None)

        # student_id = request.data.get("student_id")
        # print(current_student_id)
        if not Student.objects.filter(pk=student_id).exists():
            return Response({"Success": False,
                             "Data": ["Invalid Student id"]}, status=status.HTTP_400_BAD_REQUEST)
        student = Student.objects.get(pk=student_id)
        current_student = CurrentStudent.objects.filter(pk=current_student_id, school=school, student=student)
        student_history = StudentHistory.objects.filter(pk=current_student_id, school=school, student=student)
        if not current_student.exists() and not student_history.exists():
            return Response({"Success": False,
                             "Data": ["Invalid Student id"]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            query_set = current_student.get(pk=current_student_id)
            serializer = CurrentStudentSerializer(query_set, many=False)
        except Exception as e:
            query_set = student_history.get(pk=current_student_id)
            serializer = StudentHistorySerializer(query_set, many=False)
        return Response({"Success": True,
                         "Data": serializer.data}, status=status.HTTP_202_ACCEPTED)

    def patch(self, request, current_student_id):
        school = School.objects.get(user=request.user)
        # student_id = request.data.get("student_id")
        # print(current_student_id)
        class_id = request.data.get('class_id', None)
        section_id = request.data.get('section_id', None)
        session_id = request.data.get('session_id', None)
        registartion_no = request.data.get("registartion_no", None)
        if registartion_no:
            if CurrentStudent.objects.filter(registartion_no__iexact=registartion_no, school=school).exists():
                return Response({"Success": False,
                                 "Data": ["registartion no already exists"]}, status=status.HTTP_400_BAD_REQUEST)
        # is_valid_requst, error = valid_student_update_request(request.data)
        # if not is_valid_requst:
        #     return Response({"Success": False,
        #                      "Data": [error]}, status=status.HTTP_400_BAD_REQUEST)
        if session_id:
            if not Session.objects.filter(pk=session_id).exists():
                return Response({"Success": False,
                                 "Data": ["Invalid session id"]}, status=status.HTTP_400_BAD_REQUEST)
            session = Session.objects.get(pk=session_id)
        if section_id:
            if not ClassSection.objects.filter(pk=section_id).exists():
                return Response({"Success": False,
                                 "Data": ["Invalid section id"]}, status=status.HTTP_400_BAD_REQUEST)
            section = ClassSection.objects.get(pk=section_id)
        if class_id:
            if not SchoolClass.objects.filter(pk=class_id).exists():
                return Response({"Success": False,
                                 "Data": ["Invalid section id"]}, status=status.HTTP_400_BAD_REQUEST)
            school_class = SchoolClass.objects.get(pk=class_id)
        current_student = CurrentStudent.objects.filter(pk=current_student_id, school=school)
        if not current_student.exists():
            return Response({"Success": False,
                             "Data": ["Invalid Student id"]}, status=status.HTTP_400_BAD_REQUEST)
        current_student = current_student[0]
        student = current_student.student
        serializer = StudentSerializer(instance=student, data=request.data, partial=True)
        # print(request.data.get('registration_no'))
        if serializer.is_valid():
            registartion_no = request.data.get('registration_no', None)
            student = serializer.save()
            if section_id:
                # print(section)
                current_student.section = section
            if class_id:
                current_student.school_class = school_class
            if registartion_no:
                current_student.registration_no = registartion_no
            if session_id:
                current_student.session = session
            if section_id or class_id or registartion_no or section_id:
                current_student.save()
            # if not current_student.exists():
            return Response({"Success": True,
                             "Data": ["Student details are updated"]}, status=status.HTTP_201_CREATED)
        else:
            # if not current_student.exists():
            return Response({"Success": False,
                             "Data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, current_student_id):
    #     school = School.objects.get(user=request.user)
    #     current_student = CurrentStudent.objects.filter(pk=current_student_id, school=school)
    #     if not current_student.exists():
    #         return Response({"Success": False,
    #                          "Data": ["Invalid Student id"]}, status=status.HTTP_400_BAD_REQUEST)
    #     current_student = current_student[0]
    #     current_student.delete()
    #     return Response({"Success": True,
    #                      "Data": ["Student deleted"]}, status=status.HTTP_201_CREATED)

    def delete(self, request, current_student_id):
        school = School.objects.get(user=request.user)
        # student_id = request.data.get("student_id")
        # print(current_student_id)
        current_student = CurrentStudent.objects.filter(pk=current_student_id, school=school)
        if not current_student.exists():
            return Response({"Success": False,
                             "Data": ["Invalid Student id"]}, status=status.HTTP_400_BAD_REQUEST)
        current_student = current_student[0]
        student = current_student.student
        if not ResultCoScholasticSubjectMarks.objects.filter(
                student=student) and not ResultAcadmicsSubjectMarks.objects.filter(student=student).exists():
            user = student.user
            user.delete()
            student.delete()
        else:
            StudentHistory.objects.create(student=student, school=current_student.school,
                                          school_class=current_student.school_class, session=current_student.session,
                                          section=current_student.section,
                                          registration_no=current_student.registration_no)
        current_student.delete()
        return Response({"Success": True,
                         "Data": ["Student deleted"]}, status=status.HTTP_201_CREATED)


def get_row_list(df):
    row_list = []

    # Iterate over the rows
    for index, row in df.iterrows():
        # Extract the values of the desired columns
        values = row[['First Name', 'Middle Name', 'Last Name', 'Date of Birth', 'Email', 'Registration Number',
                      'Father Name', 'Gender', 'Session', 'Class', 'Section',
                      'Phone Number', 'Mother Name', 'Address Line 1', 'Address Line 2', 'City', 'State', 'Country',
                      'Pincode']]

        # Create a dictionary with the modified keys
        row_dict = {
            'first_name': values['First Name'],
            'middle_name': values['Middle Name'],
            'last_name': values['Last Name'],
            'parents_no': values['Phone Number'],
            'dob': values['Date of Birth'],
            'email': values['Email'],
            'registration_number': values['Registration Number'],
            'father_name': values['Father Name'],
            'gender': values['Gender'],
            'session': values['Session'],
            'class': values['Class'],
            'section': values['Section'],
            'mother_name': values['Mother Name'],
            'username': values['First Name'],
            'password': generate_random_password(),
            'address_line1': values['Address Line 1'],
            'address_line2': values['Address Line 2'],
            'city': values['City'],
            'state': values['State'],
            'country': values['Country'],
            'pincode': values['Pincode']
        }

        # Append the dictionary to the row_list
        row_list.append(row_dict)
    return row_list


def get_student_list(row_list, created_users, id):
    ids = id
    student_list = []
    for row in row_list:
        student_list.append(
            Student(
                user=created_users.get(row.get('username') + str(ids)),
                first_name=row.get('first_name', None),
                email=row.get('email', None),
                middle_name=row.get('middle_name', None),
                phone_no=row.get('phone_no', None),
                gender=row.get('gender', None),
                last_name=row.get('last_name', None),
                father_name=row.get('father_name', None),
                mother_name=row.get('mother_name', None),
                parents_no=row.get('parents_no', None),
                dob=row.get('dob', None),
                address_line1=row.get("address_line1", None),
                address_line2=row.get("address_line2", None),
                city=row.get("city", None),
                state=row.get("state", None),
                country=row.get("country", None),
                pincode=row.get("pincode", None)

            )
        )
        ids = ids + 1
    return student_list


def delete_users(users_object):
    for user in users_object:
        try:
            user.delete()
        except Exception as e:

            log.error("This error from delete_users function " + str(e))
            pass


class SchoolStudentBulkView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request):
        school = School.objects.get(user=request.user)
        class_id = request.GET.get('class_id', None)

        session_id = request.GET.get('session_id', None)

        if not CurrentClassSection.objects.filter(schoolclass__id=class_id).exists():

            return Response({"Success": False,
                             "Data": ["Invalid class id"]}, status=status.HTTP_400_BAD_REQUEST)
        class_id = CurrentClassSection.objects.filter(schoolclass__id=class_id)[0].schoolclass.pk
        if not class_id or not SchoolClass.objects.filter(pk=class_id, school=school).exists():
            return Response({"Success": False,
                             "Data": ["Invalid class id"]}, status=status.HTTP_400_BAD_REQUEST)
        if not session_id or not Session.objects.filter(pk=session_id).exists():
            return Response({"Success": False,
                             "Data": ["Invalid session"]}, status=status.HTTP_400_BAD_REQUEST)
        school_class = SchoolClass.objects.get(pk=class_id)
        session = Session.objects.get(pk=session_id)
        all_section = CurrentClassSection.objects.prefetch_related('section').filter(schoolclass=school_class,
                                                                                     session=session)
        class_data = [school_class.name]
        section_data = [c.section.section for c in all_section]
        session_data = [session.name]
        school_excel_generator_Obj = SchoolExcelGenerator()
        excel = school_excel_generator_Obj.generate_student_excel(session_data, class_data, section_data)
        # print(excel)
        # time.sleep(10)
        # excel.seek(0)
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="reportifyStudentTemplet.xlsx"'

        # Write the BytesIO content to the response
        response.write(excel.getvalue())
        return response

    def post(self, request):
        school = School.objects.get(user=request.user)
        try:
            session = Session.objects.get(pk=request.data.get('session_id'))
        except Exception as e:
            return Response({"Success": False,
                             "Data": "Invalid session id"}, status=status.HTTP_400_BAD_REQUEST)
        file = request.data.get('file')
        try:
            content = file.read()  # these are bytes
        except Exception as e:
            return Response({
                "Success": False,
                'data': "invalid file"},
                status=status.HTTP_400_BAD_REQUEST)
        file_content = ContentFile(content)
        file_name = fs.save(
            "_student.xlsx", file_content
        )
        tmp_file = fs.path(file_name)
        school_excel_generator_Obj = SchoolExcelValidator()
        # session = Session.objects
        school_students = CurrentStudent.objects.select_related('school').filter(school=school)
        current_class_sections = CurrentClassSection.objects.prefetch_related('section', 'schoolclass').filter(
            session=session, school=school)
        all_class = [current_class_section.schoolclass for current_class_section in current_class_sections]
        all_section = [current_class_section.section for current_class_section in current_class_sections]
        list_of_classes = [c.name for c in all_class]
        list_of_section = [section.section for section in all_section]
        registration_no = set()
        for school_student in school_students:
            registration_no.add(school_student.registration_no)
        # print(registration_no)
        # print(tmp_file)
        student_data = school_excel_generator_Obj.read_excel(file_path=tmp_file, sheet_name="Student Data", skiprows=1)

        is_valid = school_excel_generator_Obj.is_student_excel_valid(student_data=student_data,
                                                                     session_data=student_data.Session,
                                                                     class_data=list_of_classes,
                                                                     section_data=list_of_section,
                                                                     student_registration_set=registration_no)
        if not is_valid:
            error = school_excel_generator_Obj.generate_student_excel_errors(student_data=student_data,
                                                                             session_data=student_data.Session,
                                                                             class_data=list_of_classes,
                                                                             section_data=list_of_section,
                                                                             student_registration_set=registration_no)
            # print(html_code)

            return Response({"Success": False,
                             "Data": error}, status=status.HTTP_400_BAD_REQUEST)
        df = pd.DataFrame(student_data)
        row_list = get_row_list(df)
        # print(row_list)
        user_section_dict = {}
        users = []
        school_class = None
        sections = None

        cursor = connection.cursor()
        cursor.execute("select nextval('accounts_user_id_seq')")

        result = cursor.fetchone()
        ids = result[0]
        starting_id = ids
        # Set the sequence value
        cursor.execute(f"SELECT setval('accounts_user_id_seq', {starting_id + len(row_list)})")
        # Commit the changes to the database
        connection.commit()
        cursor.execute("select nextval('student_student_id_seq')")
        result = cursor.fetchone()
        std_id = result[0]
        # Set the sequence value
        cursor.execute(f"SELECT setval('student_student_id_seq', {std_id + len(row_list)})")

        # Commit the changes to the database
        connection.commit()
        csv_student_info = []
        user_name_dict = {}
        current_data = {}
        student_list = []
        class_dict = {}
        section_dict = {}
        current_students = []
        user_object = None
        uploaded_csv = StudentCsv.objects.create(csv=file, school=school, session=session)
        for row in row_list:
            password = generate_random_password()
            first_name = row.get('first_name')
            middle_name = row.get('middle_name', " ")
            last_name = row.get("last_name", " ")
            username = row.get("username") + str(ids)
            current_data.__setitem__(username, row)
            user_name_dict.__setitem__(username, row.get("registration_number"))
            if not middle_name:
                middle_name = " "
            if not last_name:
                last_name = " "
            csv_student_info.append({
                'Full Name': row.get('first_name') + middle_name + last_name,
                "Session": session.name,
                "Class": row.get('class'),
                "Section": row.get('section'),
                "Username": username,
                "Password": password
            })
            # print(i)
            if not user_object:
                user_object = User(
                    pk=ids,
                    username=username,
                    is_student=True,
                    password=make_password(password),
                    is_active=True,
                )

            new_user = copy.deepcopy(user_object)
            new_user.username = username
            new_user.pk = ids
            new_user.password =make_password(password)
            users.append(new_user)
            student_list.append(
                Student(
                    pk=std_id,
                    user_id=ids,
                    first_name=row.get('first_name', None),
                    email=row.get('email', None),
                    middle_name=row.get('middle_name', None),
                    phone_no=row.get('phone_no', None),
                    gender=row.get('gender', None),
                    last_name=row.get('last_name', None),
                    father_name=row.get('father_name', None),
                    mother_name=row.get('mother_name', None),
                    parents_no=row.get('parents_no', None),
                    dob=row.get('dob', None),
                    address_line1=row.get("address_line1", None),
                    address_line2=row.get("address_line2", None),
                    city=row.get("city", None),
                    state=row.get("state", None),
                    country=row.get("country", None),
                    pincode=row.get("pincode", None),
                    csv=uploaded_csv
                )
            )
            if not class_dict.__contains__(row.get('class')):
                school_class = SchoolClass.objects.get(name=row.get('class'), school=school)
                class_dict.__setitem__(row.get('class'), school_class)
            if not section_dict.__contains__(row.get('section')):
                class_section = ClassSection.objects.get(section=row.get('section'), school=school)
                section_dict.__setitem__(row.get('section'), class_section)
                # print(row.get('class'))
            current_students.append(CurrentStudent(
                user_id=ids,
                student_id=std_id,
                school=school,
                school_class=class_dict.get(row.get('class')),
                session=session,
                section=section_dict.get(row.get('section')),
                registration_no=row.get("registration_number"),
                csv=uploaded_csv
            ))
            ids = ids + 1
            std_id = std_id + 1
        try:
            users = User.objects.bulk_create(users)
            thread2 = multiprocessing.Process(target=Student.objects.bulk_create(student_list))
            thread2.start()
            thread2.join()
            thread3 = multiprocessing.Process(target=CurrentStudent.objects.bulk_create(current_students))
            thread3.start()
            creds_generator = CredentialExcelGenerator()
            excel = creds_generator.generate_excel(csv_student_info)
            thread3.join()
        except Exception as e:
            try:
                users.delete()
            except Exception as e:
                pass
            return Response({"Success": False,
                             "Data": "Please try again something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="reportifyStudentCreds.xlsx"'

        current_students = CurrentStudent.objects.filter(user__in=users)
        students = Student.objects.filter(user__in=users)

        # Write the BytesIO content to the response
        response.write(excel.getvalue())

        return response


class SchoolStudentByClassView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request):
        section_id = request.GET.get('sectionid', None)
        class_id = request.GET.get('classid', None)
        session_id = request.GET.get('session_id')
        school = School.objects.get(user=request.user)
        if not isinstance(section_id, int) and isinstance(section_id, int):
            return Response({"Success": False,
                             "Data": "Invalid class id"}, status=status.HTTP_400_BAD_REQUEST)
        if not Session.objects.filter(pk=session_id).exists():
            return Response({"Success": False,
                             "Data": "Invalid session id"}, status=status.HTTP_400_BAD_REQUEST)
        if not SchoolClass.objects.filter(pk=class_id).exists() and not ClassSection.objects.filter(
                pk=section_id).exists():
            return Response({"Success": False,
                             "Data": "Invalid class or section id id"}, status=status.HTTP_400_BAD_REQUEST)
        if not class_id and not section_id:
            return Response({"Success": True,
                             "Data": []}, status=status.HTTP_200_OK)
        session = Session.objects.get(pk=session_id)
        if not class_id:
            current_student = CurrentStudent.objects.prefetch_related('student').filter(
                section=ClassSection.objects.get(pk=section_id), session=session, school=school)
            serializer = CurrentStudentSerializer(current_student, many=True)
            return Response({"Success": True,
                             "Data": serializer.data}, status=status.HTTP_200_OK)
        if not section_id:
            current_student = CurrentStudent.objects.prefetch_related('student').filter(
                school_class=SchoolClass.objects.get(pk=class_id), session=session, school=school)
            serializer = CurrentStudentSerializer(current_student, many=True)
            return Response({"Success": True,
                             "Data": serializer.data}, status=status.HTTP_200_OK)

        current_student = CurrentStudent.objects.prefetch_related('student').filter(
            section=ClassSection.objects.get(pk=section_id), session=session,
            school_class=SchoolClass.objects.get(pk=class_id), school=school)
        serializer = CurrentStudentSerializer(current_student, many=True)
        return Response({"Success": True,
                         "Data": serializer.data}, status=status.HTTP_200_OK)


class StudentDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = Student.objects.get(user=request.user)
        current_student = CurrentStudent.objects.get(student=student)
        serializer = CurrentStudentSerializer(current_student, many=False)
        return Response({"Success": True,
                         "Data": serializer.data}, status=status.HTTP_200_OK)


class StudentEditView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def patch(self, request):
        user = request.user
        student = Student.objects.get(user=user)
        data = request.data
        serializer = StudentSerializer(instance=student, data=data, partial=True)
        if serializer.is_valid():
            student = serializer.save()
            student.save()
            return Response({"Success": True,
                             "Data": "student details updated"}, status=status.HTTP_200_OK)
        return Response({"Success": False,
                         "Data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


def permote_student(students, source_session, target_session, school):
    if not students or len(students) == 0 or not isinstance(students, list):
        return Response({"Success": False,
                         "Data": "student can't be empty"}, status=status.HTTP_400_BAD_REQUEST)
    source_class_sections = CurrentClassSection.objects.filter(school=school, session=source_session)
    target_class_sections = CurrentClassSection.objects.filter(school=school, session=target_session)
    all_student = CurrentStudent.objects.prefetch_related('student').filter(school=school)
    all_student_history = StudentHistory.objects.prefetch_related('student').filter(session=source_session)
    history_students = []
    update_student = []
    try:
        for student in students:
            current_student = all_student.get(student__id=student.get('id'))
            current_student.school_class = target_class_sections.get(schoolclass__id=student.get('target_class_id'),
                                                                     section__id=student.get(
                                                                         'target_section_id')).schoolclass
            current_student.section = target_class_sections.get(schoolclass__id=student.get('target_class_id'),
                                                                section__id=student.get('target_section_id')).section
            current_student.session = target_session
            update_student.append(current_student)

            history_students.append(
                StudentHistory(
                    student=current_student.student,
                    school=school,
                    school_class=source_class_sections.get(schoolclass__id=student.get('source_class_id'),
                                                           section__id=student.get('source_section_id')).schoolclass,
                    section=source_class_sections.get(schoolclass__id=student.get('source_class_id'),
                                                      section__id=student.get('source_section_id')).section,
                    session=source_session,
                    registration_no=current_student.registration_no
                )
            )
            if all_student_history.filter(student=current_student.student,
                                          session=source_session).exists() or all_student.filter(
                student=current_student.student, session=target_session).exists():
                return Response({"Success": False,
                                 "Data": "some student already exists in target session"},
                                status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"Success": False,
                         "Data": "invalid classs_id or section id or something else"},
                        status=status.HTTP_400_BAD_REQUEST)
    StudentHistory.objects.bulk_create(history_students)
    for student in update_student:
        student.save()
    return Response({"Success": True,
                     "Data": "Student permoted"}, status=status.HTTP_201_CREATED)


def move_student(students, source_session, target_session, school, sorted_session):
    if not students or len(students) == 0 or not isinstance(students, list):
        return Response({"Success": False,
                         "Data": "student can't be empty"}, status=status.HTTP_400_BAD_REQUEST)
    source_class_sections = CurrentClassSection.objects.filter(school=school, session=source_session)
    target_class_sections = CurrentClassSection.objects.filter(school=school, session=target_session)

    all_student_history = StudentHistory.objects.prefetch_related('student').filter(session=source_session,
                                                                                    school=school)
    all_student_history1 = StudentHistory.objects.prefetch_related('student').filter(session=target_session,
                                                                                     school=school)
    if source_session.id == sorted_session[0].id:
        all_student = CurrentStudent.objects.prefetch_related('student').filter(session=source_session, school=school)
    else:
        all_student = StudentHistory.objects.prefetch_related('student').filter(session=source_session, school=school)

    history_students = []
    history_students1 = []

    for student in students:

        real_student = all_student.get(student__id=student.get('id'))

        history_students.append(
            StudentHistory(
                student=real_student.student,
                school=school,
                school_class=target_class_sections.get(schoolclass__id=student.get('target_class_id'),
                                                       section__id=student.get('target_section_id')).schoolclass,
                section=target_class_sections.get(schoolclass__id=student.get('target_class_id'),
                                                  section__id=student.get('target_section_id')).section,
                session=target_session,
                registration_no=real_student.registration_no
            )
        )
        # history_students1.append(
        #     StudentHistory(
        #         student=real_student.student,
        #         school=school,
        #         school_class=source_class_sections.get(schoolclass__id=student.get('source_class_id'),section__id=student.get('source_section_id')).schoolclass,
        #         section=source_class_sections.get(schoolclass__id=student.get('source_class_id'),section__id=student.get('source_section_id')).section,
        #         session=source_session,
        #         registration_no=real_student.registration_no
        #     )
        # )
        if all_student_history1.filter(
                student=real_student.student, session=target_session).exists():
            return Response({"Success": False,
                             "Data": "some student already exists in target session"},
                            status=status.HTTP_400_BAD_REQUEST)
    # except Exception as e:
    #     print(e)
    #     return Response({"Success": False,
    #                      "Data": "invalid classs_id or section id or something else"},
    #                     status=status.HTTP_400_BAD_REQUEST)

    StudentHistory.objects.bulk_create(history_students)

    return Response({"Success": True,
                     "Data": "Student updated"}, status=status.HTTP_201_CREATED)


class PromoteDemoteView(APIView):

    def post(self, request):
        source_session_id = request.data.get('source_session_id', None)
        target_session_id = request.data.get('target_session_id', None)
        students = request.data.get('students', None)
        school = School.objects.get(user=request.user)
        if not source_session_id or not Session.objects.filter(pk=source_session_id).exists():
            return Response({"Success": False,
                             "Data": "inavlid source_session_id"}, status=status.HTTP_400_BAD_REQUEST)

        if not target_session_id or not Session.objects.filter(pk=target_session_id).exists():
            return Response({"Success": False,
                             "Data": "inavlid target_session_id"}, status=status.HTTP_400_BAD_REQUEST)
        target_session = Session.objects.get(pk=target_session_id)
        source_session = Session.objects.get(pk=source_session_id)
        all_session = Session.objects.all()
        sorted_session = sort_sessions_by_name(all_session)
        if target_session == source_session:
            return Response({"Success": False,
                             "Data": "you cant move in student in same session"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            if target_session_id == sorted_session[0].id:
                return permote_student(students, source_session, target_session, school)

            else:
                return move_student(students, source_session, target_session, school, sorted_session)
        except Exception as e:
            log.error("Error from promote demote " + str(e))
            return Response({"Success": False,
                             "Data": "Something went wrong with the data format"}, status=status.HTTP_400_BAD_REQUEST)


class ArchivedList(APIView):
    permission_classes = [IsAuthenticated, IsSchool]
    pagination_class = StudentPagination

    def get(self, request):
        page_size = request.GET.get('limit', None)
        session_id = request.GET.get('session_id', None)
        school = School.objects.get(user=request.user)

        sessions = Session.objects.all()
        short_sessions = sort_sessions_by_name(sessions)
        if not session_id or not Session.objects.filter(pk=session_id).exists():
            session = short_sessions[0]
        else:
            session = Session.objects.get(pk=session_id)
        # Exclude student history records that match any of the current students
        current = CurrentStudent.objects.filter(school=school)
        excluded_history = StudentHistory.objects.filter(
            student__in=current.values('student'),
        )

        # Final result with excluded student history
        filtered_history = StudentHistory.objects.filter(school=school, session=session).exclude(
            pk__in=excluded_history)

        paginator = self.pagination_class()
        if page_size:
            paginator.page_size = page_size
        paginated_queryset = paginator.paginate_queryset(filtered_history, request)
        serialized_data = StudentHistorySerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serialized_data.data)


class CsvView(APIView):
    permission_classes = [IsAuthenticated, IsSchool]

    def get(self, request):
        school = School.objects.get(user=request.user)
        student_csv = StudentCsv.objects.filter(school=school)
        serializer = StudentCsvSerializer(student_csv, many=True)
        return Response({"Success": True,
                         "Data": serializer.data}, status=status.HTTP_202_ACCEPTED)

    def delete(self,request,csv_id):
        if not StudentCsv.objects.filter(pk=csv_id).exists():
            return Response({"Success": False,
                             "Data":" invalid id"}, status=status.HTTP_400_BAD_REQUEST)
        csv = StudentCsv.objects.get(pk=csv_id)
        users = []
        students =Student.objects.filter(csv=csv)
        for student in students:
            if ResultCoScholasticSubjectMarks.objects.filter(student=student).exists() or ResultAcadmicsSubjectMarks.objects.filter(student=student).exists():
                return Response({"Success": False,
                                 "Data": " You can delete these student result is assosiated with it"}, status=status.HTTP_400_BAD_REQUEST)
            users.append(student.user)
        for user in users:
            user.delete()
        csv.delete()
        return Response({"Success": True,
                         "Data": " Deleted successfult"},
                        status=status.HTTP_200_OK)


class InfoView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self,request):
        student = Student.objects.get(user=request.user)
        current_student = None
        try:
            current_student = CurrentStudent.objects.get(student=student)
        except Exception as e:
            sessions = Session.objects.all()
            sorted_session = sort_sessions_by_name(sessions)
            for session in sorted_session:
                if StudentHistory.objects.filter(student=student,session=session).exists():
                    current_student = StudentHistory.objects.get(student=student,session=session)
                    break

        student_details = {
            'address':student.address_line1 ,
            'contact_no':student.phone_no,
            'dob':student.dob,
            'email':student.email,
            'father_name':student.father_name,
            'first_name':student.first_name,
            'gender':student.gender,
            'image':str(student.profile_image),
            'last_name':student.last_name,
            'mother_name':student.mother_name,
            'student_id':student.pk
        }
        try:
            current_class = {
                'class_name':current_student.school_class.name ,
                'section_name':current_student.section.section,
                'class_id':"class_id",
                "archive":False,
                'id':current_student.pk,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'roll_no':"",
                "session_name":current_student.session.name
            }
        except Exception as E:
            current_class = {
                'class_name':" ",
                'class_id': "",
                "archive": False,
                'id':"",
                'first_name': student.first_name,
                'last_name': student.last_name,
                'roll_no': "",
                "session_name": ""
            }
        data = [{
            'student_details':student_details,
            'current_class':current_class
        }]
        return Response({"Success": True,
                         "Data":data },
                        status=status.HTTP_200_OK)


class SessionView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self,request):
        session = Session.objects.all()
        sorted_session = sort_sessions_by_name(session)
        data = [session.name for session in sorted_session]
        return Response({"Success": True,
                         "Data": data},
                        status=status.HTTP_200_OK)


class TestView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = Student.objects.get(user=request.user)
        sessions = Session.objects.all()
        sorted_session = sort_sessions_by_name(sessions)

        result =[]

        for session in sorted_session:
            tests = ResultAcadmicsSubjectMarks.objects.filter(student=student,session=session)

            for test in tests:
                if test.test.test not in result:
                    result.append(test.test.test)

        return Response({"Success": True,
                         "Data": result},
                        status=status.HTTP_200_OK)