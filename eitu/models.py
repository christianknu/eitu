from django.db import models  # to facilitate integration

class wifi_occupancy(models.Model):
    room_name = models.CharField(max_length=255)
    room_occupancy = models.IntegerField()
    timestamp = models.CharField(max_length=255)


class TimeEditEvent(models.Model):
    uid = models.CharField(max_length=255)
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField()
    datetime_stamp = models.DateTimeField()
    datetime_lastModified = models.DateTimeField()
    summary = models.TextField()
    location = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
