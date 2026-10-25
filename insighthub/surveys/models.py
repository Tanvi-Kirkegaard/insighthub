from django.db import models
from catalogue.models import Topic

class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    topic = models.ForeignKey(
        Topic,
        on_delete=models.PROTECT,
        related_name='surveys'
    )

    launch_date = models.DateField()
    expiration_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Choice(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text


class Question(models.Model):
    TEXT = 'text'
    SINGLE_CHOICE = 'single_choice'
    MULTIPLE_CHOICE = 'multiple_choice'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (SINGLE_CHOICE, 'Single choice'),
        (MULTIPLE_CHOICE, 'Multiple choice'),
    ]

    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
    )

    text = models.TextField()
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default=TEXT,
    )

    choices = models.ManyToManyField(
        Choice,
        blank=True,
        related_name='questions',
    )

    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.text



