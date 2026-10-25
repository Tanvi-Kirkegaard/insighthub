from django import forms
from .models import Survey, Question, Choice
from django.utils import timezone

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ('title', 'description', 'topic', 'launch_date', 'expiration_date')

        labels = {
            'title': 'Survey title',
            'description': 'Survey description',
            'topic': 'Survey topic',
            'launch_date': 'Launch date',
            'expiration_date': 'Expiration date',
        }

        help_text = {
            'title': 'Enter a descriptive title for the survey.',
            'description': 'Briefly describe the purpose of the survey.',
            'topic': 'Select the topic that this survey belongs to.',
            'launch_date': 'Select the date when the survey will be launched.',
            'expiration_date': 'Select the date when the survey will expire.',
        }

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a survey title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the purpose of this survey', 'rows': 4}),
            'launch_date': forms.DateInput(attrs={'type': 'date'}),
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        super().clean()

        launch_date = self.cleaned_data.get('launch_date')
        expiration_date = self.cleaned_data.get('expiration_date')

        if (
            launch_date is not None
            and not self.instance.pk
            and launch_date < timezone.localdate()
        ):
            raise forms.ValidationError("The launch date cannot be in the past.")

        if (
            launch_date is not None
            and expiration_date is not None
            and expiration_date <= launch_date
        ):
            raise forms.ValidationError("Expiration date must be after the launch date.")

        return self.cleaned_data

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
            'survey',
            'text',
            'question_type',
            'choices',
            'is_required',
            'order'
        ]

        labels = {
            'survey': 'Survey',
            'text': 'Question text',
            'question_type': 'Question type',
            'choices': "Answer choices",
            'is_required': 'Required',
            'order': 'Display order',
        }

        help_text = {
            'text': 'Enter the question that will be shown to participants.',
            'question_type': 'Select the type of question (text, single choice, or multiple choice).',
            'is_required': 'Indicate whether this question is required to be answered.',
            'order': 'Specify the order of this question in the survey.',
        }

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Enter the question...', 'rows': 3}),
            'question_type': forms.Select(),
            'choices': forms.CheckboxSelectMultiple(),
            'is_required': forms.CheckboxInput(),
            'order': forms.NumberInput(attrs={'min': 1}),
        }

    def clean_text(self):
        text = self.cleaned_data['text'].strip()

        if len(text) < 10:
            raise forms.ValidationError(
                "The question must contain at least 10 characters.")

        return text


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = [
            "text",
        ]
        labels = {
            "text": "Answer option",
        }
        widgets = {
            "text": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Very satisfied",
                }
            ),
        }

    def clean_text(self):
        text = self.cleaned_data["text"].strip()

        if len(text) < 2:
            raise forms.ValidationError(
                "The choice must contain at least 2 characters."
            )

        return text