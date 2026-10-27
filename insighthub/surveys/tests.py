from django.template.defaulttags import url
from django.test import TestCase
from datetime import timedelta, date
from django.utils import timezone
from catalogue.models import Topic
from .models import Survey, Question, Choice
from django.urls import reverse


class SurveyViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            title="Test Topic",
            description="This is a test topic."
        )

        self.survey = Survey.objects.create(
            title="Test Survey",
            description="This is a test survey.",
            topic=self.topic,
            launch_date=timezone.localdate(),
            expiration_date=timezone.localdate() + timedelta(days=7)
        )

    def test_survey_list_displays_specific_survey(self):
        url = reverse(
            'surveys:survey-detail', kwargs={'pk': self.survey.pk},
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surveys/survey_detail.html")

        self.assertContains(response, self.survey.title)
        self.assertContains(response, self.survey.description)


    def test_survey_creation_with_valid_data(self):
        url_variable = reverse('surveys:survey-create')

        response = self.client.post(
            url_variable,
            {
            'title': 'New Survey',
            'description': 'New Survey Description',
            'topic': self.topic.pk,
            'launch_date': timezone.localdate(),
            'expiration_date': timezone.localdate() + timedelta(days=7)
        }
    )

        self.assertEqual(Survey.objects.count(), 2)  # Redirect after successful creation
        self.assertTrue(Survey.objects.filter(title='New Survey').exists())
        self.assertRedirects(response, reverse('surveys:survey-list'))

    def test_survey_detail_displays_specific_survey(self):
        response = self.client.get(
            reverse(
            'surveys:survey-detail', kwargs={'pk': self.survey.pk},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "surveys/survey_detail.html")
        self.assertContains(response, self.survey.title)
        self.assertContains(response, self.survey.description)


    def test_survey_creation_with_invalid_data(self):
        response = self.client.post(
            reverse('surveys:survey-create'),
            {
                'title': 'New Survey',  # Invalid: title is required
                'description': 'A newly created test survey.',
                'topic': self.topic.pk,
                'launch_date': timezone.localdate(),
                'expiration_date': timezone.localdate() + timedelta(days=14)
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Survey.objects.filter(title='New Survey').exists())
        self.assertRedirects(response, reverse('surveys:survey-list'))

    def test_survey_update_with_valid_data(self):
        response = self.client.post(
            reverse(
                'surveys:survey-update', kwargs={'pk': self.survey.pk}
            ),
            {
                'title': 'Updated Survey',
                'description': 'Updated Survey Description',
                'topic': self.topic.pk,
                'launch_date': self.survey.launch_date,
                'expiration_date': self.survey.expiration_date
            },
        )

        self.survey.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.survey.title, 'Updated Survey')
        self.assertEqual(self.survey.description, 'Updated Survey Description')
        self.assertRedirects(response, reverse('surveys:survey-list'))


    def test_survey_delete_removes_survey(self):
        response = self.client.post(
            reverse(
                'surveys:survey-delete', kwargs={'pk': self.survey.pk}
            )
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Survey.objects.filter(pk=self.survey.pk).exists())
        self.assertRedirects(response, reverse('surveys:survey-list'))


    def test_survey_create_rejects_expiration_before_launch(self):
        response = self.client.post(
            reverse('surveys:survey-create'),
            {
                'title': 'Invalid Schedule Survey',
                'description': 'This survey has an invalid dates.',
                'topic': self.topic.pk,
                'launch_date': timezone.localdate() + timedelta(days=7),
                'expiration_date': timezone.localdate() + timedelta(days=3)  # Expiration before launch
            },
        )

        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(Survey.objects.filter(title='Invalid Schedule Survey').exists())
        self.assertContains(response, "Expiration date must be after the launch date.")


    def test_survey_create_rejects_past_launch_date(self):
        response = self.client.post(
            reverse('surveys:survey-create'),
            {
                'title': 'Past Survey',
                'description': 'Survey with an invalid launch date.',
                'topic': self.topic.pk,
                'launch_date': timezone.localdate() - timedelta(days=1),  # Past launch date
                'expiration_date': timezone.localdate() + timedelta(days=7)
            },
        )

        self.assertEqual(response.status_code, 200)  # Form re-rendered with errors
        self.assertFalse(Survey.objects.filter(title='Past Survey').exists())
        self.assertContains(response, "The launch date cannot be in the past.")


class QuestionViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            title='Test Topic',
            description='Test Description',
        )

        self.survey = Survey.objects.create(
            title='Test Survey',
            description='Test Survey Description',
            topic=self.topic,
            launch_date=date.today(),
            expiration_date=date.today() + timedelta(days=7),
        )

    def test_question_creation(self):
        response = self.client.post(
            reverse(
                'surveys:question-create',
                kwargs={'survey_pk': self.survey.pk},
            ),
            {
                "survey": self.survey.pk,
                "text": "How useful was this survey?",
                "question_type": "text",
                "is_required": True,
                "order": 1,
            },
        )

        self.assertTrue(Question.objects.filter(
            text="How useful was this survey?").exists()
        )

        question = Question.objects.get(text="How useful was this survey?")
        self.assertEqual(question.survey, self.survey)


    def test_question_update(self):
        question = Question.objects.create(
            survey = self.survey,
            text="How useful was this survey?",
            question_type="text",
            is_required=True,
            order=1,
        )

        response = self.client.post(
            reverse(
                "surveys:question-update",
                kwargs={'pk': question.pk}
            ),
            {"survey": self.survey.pk,
                "text": "How useful was the updated survey?",
                "question_type": "text",
                "is_required": True,
                "order": 1,
            }
        )

        question.refresh_from_db()

        self.assertEqual(
            question.text,
            "How useful was the updated survey?"
        )

        self.assertEqual(Question.objects.count(), 1)


    def test_question_delete(self):
        question = Question.objects.create(
            survey = self.survey,
            text="How useful was this survey?",
            question_type="text",
            is_required=True,
            order=1,
        )

        response = self.client.post(
            reverse(
                "surveys:question-delete",
                kwargs={'pk': question.pk}
            ),
        )

        self.assertFalse(
            Question.objects.filter(pk=question.pk).exists()
        )

    def test_question_creation_rejects_short_text(self):
        response = self.client.post(
            reverse(
                "surveys:question-create",
                kwargs={"survey_pk": self.survey.pk},
            ),
            {
                "survey": self.survey.pk,
                "text": "Short",
                "question_type": "text",
                "is_required": True,
                "order": 1,
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            Question.objects.filter(text="Short").exists()
        )

        self.assertContains(
            response,
            "The question must contain at least 10 characters.",
        )

    def test_survey_detail_displays_question(self):
        Question.objects.create(
            survey=self.survey,
            text="How useful was this survey?",
            question_type="text",
            is_required=True,
            order=1,
        )

        response = self.client.get(
            reverse(
                "surveys:survey-detail",
                kwargs={'pk': self.survey.pk}
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "How useful was this survey?")


    def test_choice_creation(self):
        response = self.client.post(
            reverse("surveys:choice-create"),
            {
                "text": "Very satisfied"
            }
        )

        self.assertEqual(Choice.objects.count(), 1)
        self.assertEqual(
            Choice.objects.get(text="Very satisfied").text,
            "Very satisfied",
        )
        self.assertRedirects(
            response,
            reverse("surveys:survey-list"),
        )

    def test_question_creation_with_choice(self):
        choice_one = Choice.objects.create(
            text="Very satisfied",
        )

        choice_two = Choice.objects.create(
            text="Satisfied",
        )

        response = self.client.post(
            reverse(
                "surveys:question-create",
                kwargs={"survey_pk": self.survey.pk},
            ),
            {
                "survey": self.survey.pk,
                "text": "How satisfied are you with this survey?",
                "question_type": Question.SINGLE_CHOICE,
                "choices": [choice_one.pk, choice_two.pk],
                "is_required": True,
                "order": 1,
            },
        )
        question = Question.objects.get(
            text="How satisfied are you with this survey?")

        self.assertEqual(question.choices.count(), 2)
        self.assertIn(choice_one, question.choices.all())
        self.assertIn(choice_two, question.choices.all())
        self.assertRedirects(
            response,
            reverse("surveys:survey-list"),
        )