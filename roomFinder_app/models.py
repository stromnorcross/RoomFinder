from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=50)
    room_location = models.CharField(max_length=100)

    def __str__(self):
        return self.room_name

class Reservation(models.Model):
    room = models.ManyToManyField(Room, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, on_delete=models.CASCADE)



class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    user_type = models.TextChoices("user_type", "USER ADMIN")
