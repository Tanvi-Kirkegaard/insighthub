from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def short_description(value):
    if len(value) > 100:
        return value[:100] + '...'
    return value

@register.filter
def survey_status(survey):
    today = timezone.localdate()

    if today < survey.launch_date:
        return "Upcoming"

    if today > survey.expiration_date:
        return "Closed"

    return "Open"