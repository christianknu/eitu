from django.http import HttpResponse
import logging
from eitu.core import fetch_schedules, render, fetch_wifi


def index(request):
    # Logging
    logging.getLogger().setLevel(logging.INFO)

    schedules = fetch_schedules()
    wifi = fetch_wifi()
    html = render(schedules, wifi)

    return HttpResponse(html)
