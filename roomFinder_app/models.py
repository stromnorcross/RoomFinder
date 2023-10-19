import datetime

from django.db import models
from django.utils import timezone


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=50)
    room_location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.room_name


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    user_type = models.TextChoices("user_type", "USER ADMIN")

    def __str__(self):
        return self.name + " - " + self.email


class Reservation(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.created_at <= now

    def __str__(self):
        return self.user + " - " + self.room



