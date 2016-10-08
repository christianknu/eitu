from django.http import HttpResponse
import logging
from eitu.eitu import fetch_schedules, render, fetch_wifi


def hello(request):
    # Logging
    logging.getLogger().setLevel(logging.INFO)

    schedules = fetch_schedules()
    wifi = fetch_wifi()
    html = render(schedules, wifi)

    return HttpResponse(html)
