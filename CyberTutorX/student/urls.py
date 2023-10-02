from django.urls import path

from result.views import TempView
from .views import SchoolStudentView, SchoolStudentByIdView, SchoolStudentBulkView, SchoolStudentByClassView, \
    StudentDetailsView, StudentEditView, PromoteDemoteView, ArchivedList, CsvView, InfoView, SessionView,TestView

urlpatterns = [
    path('add/', SchoolStudentView.as_view(), name="student"),
    path('get/csv/', CsvView.as_view(), name="student"),
    path('delete/csv/<int:csv_id>/', CsvView.as_view(), name="student"),
    path('get/all/', SchoolStudentView.as_view(), name="student"),
    path('edit/<current_student_id>/', SchoolStudentByIdView.as_view(), name="edit student"),
    path('delete/<current_student_id>/', SchoolStudentByIdView.as_view(), name="edit student"),
    path('add/bulk/csv/', SchoolStudentBulkView.as_view(), name="bulk student"),
    path('get/bulk/csv/', SchoolStudentBulkView.as_view(), name="bulk student"),
    path('get/student/', SchoolStudentByClassView.as_view(),
         name="get students by class"),
    path('get/student/details/<current_student_id>', SchoolStudentByIdView.as_view(), name="get  student by id"),
    path("get/details/", StudentDetailsView.as_view(), name="get student details"),
    path("update/student_details/", StudentEditView.as_view(), name="edit student "),
    path("promote-demote/", PromoteDemoteView.as_view(), name="add student"),
    path("get/archived/student/", ArchivedList.as_view(), name="get archived list"),
    path("get/info/", InfoView.as_view(), name="get info"),
    path("get/session/", SessionView.as_view(), name="get info"),
    path("get/test/", TestView.as_view(), name="get info"),
    path("update/profile/", StudentEditView.as_view(), name="get info"),
]
