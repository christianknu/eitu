from django.http import HttpResponse
import logging, time, os
import eitu


def hello(request):
    FREQ_FETCH = 60 * 60
    FREQ_RENDER = 60
    OUT_DIR = os.getenv('EITU_OUT_DIR', '.')

    # Logging
    logging.getLogger().setLevel(logging.INFO)

    schedules = None
    last_fetch = 0

    if not schedules or time.time() - last_fetch > FREQ_FETCH:
        schedules = eitu.fetch_schedules()
        last_fetch = time.time()
    wifi = eitu.fetch_wifi()
    html = eitu.render(schedules, wifi)
    return HttpResponse(html)
