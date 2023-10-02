from django.urls import path, include
from .views import AddSessionView, GetAllSessionView

urlpatterns = [
    path("add/", AddSessionView.as_view(), name="add_session"),
    path("get/all/", GetAllSessionView.as_view(), name="all_session"),


]
