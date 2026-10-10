from django.views.generic import TemplateView

class HomePageView(TemplateView):
    """Display the InsightHub homepage."""
    template_name = "core/home.html"
