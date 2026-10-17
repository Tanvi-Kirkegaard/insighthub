from django.test import TestCase
from django.urls import reverse

from.models import Topic

class TopicViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            title="Test Topic", description="Test Description")

    def test_topic_list_view(self):
        response = self.client.get(reverse("catalogue:topic-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")

    def test_topic_detail_view(self):
        response = self.client.get(reverse("catalogue:topic-detail", kwargs={"pk": self.topic.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")
        self.assertContains(response, "Test Description")

    def test_topic_create_view(self):
        response = self.client.post(reverse("catalogue:topic-create"), {
            "title": "New Topic",
            "description": "New Description"
        })
        self.assertRedirects(response, reverse("catalogue:topic-list"))  # Redirect to the right place after successful creation
        self.assertTrue(Topic.objects.filter(title="New Topic").exists())

    def test_topic_update_view(self):
        response = self.client.post(reverse("catalogue:topic-update", kwargs={"pk": self.topic.pk}), {
            "title": "Updated Topic",
            "description": "Updated Description"
        })
        self.topic.refresh_from_db()
        self.assertRedirects(response, reverse("catalogue:topic-list"))
        self.assertEqual(self.topic.title, "Updated Topic")
        self.assertEqual(self.topic.description, "Updated Description")

    def test_topic_delete_view(self):
        response = self.client.post(reverse("catalogue:topic-delete", kwargs={"pk": self.topic.pk}))
        self.assertRedirects(response, reverse("catalogue:topic-list"))
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())


    def test_topic_create_rejects_duplicate_title(self):
        response = self.client.post(reverse("catalogue:topic-create"), {
            "title": "test topic",
            "description": "Another Description"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Topic.objects.count(), 1)
        self.assertContains(response, "A topic with this title already exists.")

    def test_topic_update_allows_unchanged_title(self):
        response = self.client.post(reverse("catalogue:topic-update", kwargs={"pk": self.topic.pk}), {
            "title": "Test Topic",
            "description": "Updated Description"
        })
        self.topic.refresh_from_db()
        self.assertRedirects(response, reverse("catalogue:topic-list"))
        self.assertEqual(self.topic.title, "Test Topic")
        self.assertEqual(self.topic.description, "Updated Description")

    def test_topic_update_rejects_duplicate_title(self):
        another_topic = Topic.objects.create(
            title="Another Topic", description="Another Description")

        response = self.client.post(reverse("catalogue:topic-update", kwargs={"pk": self.topic.pk}), {
            "title": another_topic.title,
            "description": "Updated Description"
        })

        self.topic.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.topic.title, "Test Topic")  # Ensure the title hasn't changed
        self.assertContains(response, "A topic with this title already exists.")
