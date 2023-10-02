from django.urls import path
from .views import QuizView, ExplainationView, OCRView, ChatView

urlpatterns = [
    path('Explaination/', ExplainationView.as_view(), name="quiz"),
    path('SolveByImage/', OCRView.as_view(), name="quiz"),
    path('', ChatView.as_view(), name="quiz"),
]
