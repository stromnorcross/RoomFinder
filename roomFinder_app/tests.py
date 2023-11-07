import datetime

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Room, Reservation


def create_room(name, building):
    """
    Create a room with the given 'name', 'building'
    """
    return Room.objects.create(room_name=name, building=building)


def create_user(username, email, password):
    """
    Create a user with given 'name', 'email', and 'type'
    """
    return User.objects.create_user(username=username, email=email, password=password)


class ReservationModelTests(TestCase):
    def test_was_created_recently_with_future_reservation(self):
        """
        was_created_recently() returns False for reservations whose created_at
        is in the future.
        """
        title = "Studying for Midterm"
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")

        time = timezone.now() + datetime.timedelta(days=30)
        start = timezone.now()
        end = timezone.now() + datetime.timedelta(hours=2)
        day = 1

        future_res = Reservation(title=title, room=room, user=user, start_time=start, end_time=end, day=day, created_at=time)
        self.assertIs(future_res.was_created_recently(), False)
    
    def test_was_created_recently_with_old_reservation(self):
        """
        was_created_recently() returns False for reservations whose created_at
        is older than 1 day.
        """
        title = "Studying for Midterm"
        room = create_room("Rice 130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")

        start = timezone.now()
        end = timezone.now() + datetime.timedelta(hours=2)
        day = 1
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_res = Reservation(title=title, room=room, user=user, start_time=start, end_time=end, day=day, created_at=time)
        self.assertIs(old_res.was_created_recently(), False)

    def test_was_created_recently_with_recent_reservation(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        title = "Studying for Midterm"
        room = create_room("Rice 130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")

        start = timezone.now()
        end = timezone.now() + datetime.timedelta(hours=2)
        day = 1
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_res = Reservation(title=title, room=room, user=user, start_time=start, end_time=end, day=day, created_at=time)
        self.assertIs(recent_res.was_created_recently(), True)