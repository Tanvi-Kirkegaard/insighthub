from django.shortcuts import render
from .models import Topic
from django.http import HttpRequest, HttpResponse

# Views created here:

def topic_list(request: HttpRequest) -> HttpResponse:
    """ Display all topics in the catalogue."""
    topics = Topic.objects.all()
    context = {
        'topics': topics,
    }
    return render(request, 'catalogue/topic_list.html', context)

