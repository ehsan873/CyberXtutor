from django.urls import path, include

from .views import SchoolView,UpdateSchoolView,AdminSchooView

urlpatterns = [
    path('get/details/', SchoolView.as_view(), name='get_school_details'),
    path('upload/logo/', SchoolView.as_view(), name="upload logo"),
    path("edit/school/details/",UpdateSchoolView.as_view(),name="update school details"),
    path("get/schools/",AdminSchooView.as_view(),name="get list if school")

]
