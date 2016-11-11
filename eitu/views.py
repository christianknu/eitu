from django.http import HttpResponse, JsonResponse
import logging
from eitu.core import fetch_schedules, render, fetch_wifi

import eitu.constants as constants
import eitu.formaters as formaters
from datetime import datetime

import json

def index(request):
    # Logging
    logging.getLogger().setLevel(logging.INFO)

    schedules = fetch_schedules()
    wifi = fetch_wifi()
    html = render(schedules, wifi)

    return HttpResponse(html)

