import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
#from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=100)
    building = models.CharField(max_length=100)

    def __str__(self):
        return str(self.room_name) + " " + self.building
    

class Reservation(models.Model):
    title = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def __str__(self):
        return self.title + ": " + str(self.user) + " - " + str(self.room)



