from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path("topics/", views.topic_list, name="topic-list"),
]