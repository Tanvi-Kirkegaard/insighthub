from django.urls import path
from .views import (SurveyListView, SurveyCreateView, SurveyDetailView, SurveyUpdateView, SurveyDeleteView,
                    QuestionCreateView, QuestionUpdateView, QuestionDeleteView, ChoiceCreateView)

app_name = 'surveys'

urlpatterns = [
    path("", SurveyListView.as_view(), name="survey-list"),
    path("create/", SurveyCreateView.as_view(), name="survey-create"),
    path("<int:pk>/", SurveyDetailView.as_view(), name="survey-detail"),
    path("<int:pk>/edit/", SurveyUpdateView.as_view(), name="survey-update"),
    path("<int:pk>/delete/", SurveyDeleteView.as_view(), name="survey-delete"),
    path("questions/create/", QuestionCreateView.as_view(), name="question-create"),
    path("questions/<int:pk>/edit/", QuestionUpdateView.as_view(), name="question-update"),
    path("questions/<int:pk>/delete/", QuestionDeleteView.as_view(), name="question-delete"),
    path("choices/create/", ChoiceCreateView.as_view(), name="choice-create"),
]