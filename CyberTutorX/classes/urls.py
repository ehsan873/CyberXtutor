from django.urls import path
from .views import ClassView, ClassSectionByIdView, SectionView, CurrentClass,UpdateClassSectionView,AdminClassView

urlpatterns = [
    path("get/all/", ClassView.as_view(), name="get all classes"),
    path("get/classes/section/", CurrentClass.as_view(), name="get all current class and section"),
    path("get/classes/", AdminClassView.as_view(), name="get all current class and section"),
    path("add/class/", CurrentClass.as_view(), name="add class"),
    path("update/section/<class_section_id>/", ClassSectionByIdView.as_view(), name="get_session_id"),
    path("edit/class/section/<class_section_id>",UpdateClassSectionView.as_view(),name="update class and section"),
    path("delete/class/section/<class_section_id>",UpdateClassSectionView.as_view(),name="update class and section"),
]
