from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from catalogue.models import Topic
from .models import Survey, Question, Choice
from .forms import SurveyForm, QuestionForm, ChoiceForm
from django.urls import reverse_lazy

class SurveyListView(ListView):
    model = Survey
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'

    def get_queryset(self):
        queryset = super().get_queryset()

        topic = self.request.GET.get('topic')
        sort = self.request.GET.get('sort')

        if topic:
            queryset = queryset.filter(topic_id=topic)

        if sort == "launch":
            queryset = queryset.order_by('launch_date')
        elif sort == "expiration":
            queryset = queryset.order_by('expiration_date')
        elif sort == "newest":
            queryset = queryset.order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["topics"] = Topic.objects.all()
        context["selected_topic"] = self.request.GET.get('topic', '')
        context["selected_sort"] = self.request.GET.get('sort', '')
        return context


class SurveyCreateView(CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    success_url = reverse_lazy('surveys:survey-list')

class SurveyDetailView(DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'

class SurveyUpdateView(UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    success_url = reverse_lazy('surveys:survey-list')

class SurveyDeleteView(DeleteView):
    model = Survey
    template_name = 'surveys/survey_confirm_delete.html'
    context_object_name = 'survey'
    success_url = reverse_lazy('surveys:survey-list')


class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'surveys/question_form.html'
    success_url = reverse_lazy('surveys:survey-list')

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = 'surveys/question_form.html'
    success_url = reverse_lazy('surveys:survey-list')

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'surveys/question_confirm_delete.html'
    context_object_name = 'question'
    success_url = reverse_lazy('surveys:survey-list')


class ChoiceCreateView(CreateView):
    model = Choice
    form_class = ChoiceForm
    template_name = "surveys/choice_form.html"
    success_url = reverse_lazy('surveys:question-create')


