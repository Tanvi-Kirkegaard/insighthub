from django.test import TestCase
from django.urls import reverse

class HomePageViewTests(TestCase):
    def test_homepage_returns_successful_response(self):
        """Test that the homepage view returns a 200 status code and uses the correct template."""
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)

    def test_homepage_uses_correct_template(self):
        """Test that the homepage view uses the correct template."""
        response = self.client.get(reverse("core:home"))

        self.assertTemplateUsed(response, "core/home.html")

    def test_homepage_contains_catalogue_link(self):
        """Test that the homepage view contains a link to the catalogue."""
        response = self.client.get(reverse("core:home"))
        catalogue_url = reverse("catalogue:topic-list")

        self.assertContains(response, f'href="{catalogue_url}"')