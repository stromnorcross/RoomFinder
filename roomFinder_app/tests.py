import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Room, User, Reservation


def create_room(name, location, cap):
    """
    Create a room with the given 'name', 'location', and 'cap'
    """
    return Room.objects.create(room_name=name, room_location=location, capacity=cap)


def create_user(name, email):
    """
    Create a user with given 'name', 'email', and 'type'
    """
    return User.objects.create(name=name, email=email)


class ReservationModelTests(TestCase):
    def test_was_created_recently_with_future_reservation(self):
        """
        was_created_recently() returns False for reservations whose created_at
        is in the future.
        """
        room = create_room("Rice 130", "Rice Hall", 100)
        user = create_user("Bob", "email@email.com")

        time = timezone.now() + datetime.timedelta(days=30)
        start = timezone.now()
        end = timezone.now() + datetime.timedelta(hours=2)

        future_res = Reservation(room=room, user=user, start_time=start, end_time=end, created_at=time)
        self.assertIs(future_res.was_created_recently(), False)
    
    def test_was_created_recently_with_old_reservation(self):
        """
        was_created_recently() returns False for reservations whose created_at
        is older than 1 day.
        """
        room = create_room("Rice 130", "Rice Hall", 100)
        user = create_user("Bob", "email@email.com")

        start = timezone.now()
        end = timezone.now() + datetime.timedelta(hours=2)
        
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_res = Reservation(room=room, user=user, start_time=start, end_time=end, created_at=time)
        self.assertIs(old_res.was_created_recently(), False)
