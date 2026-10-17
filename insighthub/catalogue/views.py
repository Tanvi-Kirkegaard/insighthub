from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Topic
from .forms import TopicForm
from django.urls import reverse_lazy

class TopicListView(ListView):
    """Display the topics in the catalogue as a list."""
    model = Topic
    template_name = "catalogue/topic_list.html"
    context_object_name = "topics"

class TopicDetailView(DetailView):
    """Display the details of a single topic."""
    model = Topic
    template_name = "catalogue/topic_detail.html"
    context_object_name = "topic"

class TopicCreateView(CreateView):
    form_class = TopicForm
    template_name = "catalogue/topic_form.html"
    success_url = reverse_lazy("catalogue:topic-list")

class TopicUpdateView(UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "catalogue/topic_form.html"
    success_url = reverse_lazy("catalogue:topic-list")

class TopicDeleteView(DeleteView):
    model = Topic
    template_name = "catalogue/topic_confirm_delete.html"
    success_url = reverse_lazy("catalogue:topic-list")