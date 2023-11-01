import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
#from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=50)
    room_location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.room_name
    

class Reservation(models.Model):
    title = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    day = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False, editable=False)

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def __str__(self):
        return self.title + ": " + self.user + " - " + self.room



