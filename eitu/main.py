#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging, time, os
import eitu

FREQ_FETCH = 60 * 60
FREQ_RENDER = 60
OUT_DIR = os.getenv('EITU_OUT_DIR', '.')

# Logging
logging.getLogger().setLevel(logging.INFO)

schedules = None
last_fetch = 0

while True:
    if not schedules or time.time() - last_fetch > FREQ_FETCH:
        schedules = eitu.fetch_schedules()
        last_fetch = time.time()
    wifi = eitu.fetch_wifi()
    html = eitu.render(schedules, wifi)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, 'index.html'), 'w+') as f: f.write(html)
    time.sleep(FREQ_RENDER)
