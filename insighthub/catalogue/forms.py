from django import forms

from .models import Topic

class TopicForm(forms.ModelForm):
    """Form for creating and updating topics."""
    class Meta:
        model = Topic
        fields = ['title', 'description']

        labels = {
            'title': 'Topic Title',
            'description': 'Description',
        }

        help_texts = {
            'title': 'Give the topic a clear and concise title.',
            'description': 'Briefly describe what this topic covers.',
        }

        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter a topic title...'}
            ),
            'description': forms.Textarea(
                attrs={'placeholder': 'Enter a brief description...'}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()

        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long."
            )

        queryset = Topic.objects.filter(title__iexact=title)

        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise forms.ValidationError("A topic with this title already exists."
            )

        return title