from django.db import models  # to facilitate integration

class wifi_occupancy(models.Model):
    room_name = models.CharField(max_length=255)
    room_occupancy = models.IntegerField()
    timestamp = models.CharField(max_length=255)

 #   def __str__(self):
 #       return ' '.join([self.room_name, str(self.room_occupancy), str(self.timestamp)])