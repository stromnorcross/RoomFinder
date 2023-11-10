import datetime


from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.urls import reverse
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

class MakeResTests(TestCase):
    def test_same_reservation_time(self):
        """
        Both reservations have same user, day, and room
        Reservation 1: 9:00 - 10:00
        Reservation 2: 9:00 - 10:00
        Expected Output: 1 reservation object, second reservation does not get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building':'Rice Hall', 'room_name':'130','start_time':'09:00','end_time':'10:00','day':'1',
            'title':'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 1)

    def test_same_reservation_time_different_room(self):
        """
        Both reservations have same user, day, but different rooms
        Reservation 1: 9:00 - 10:00
        Reservation 2: 9:00 - 10:00
        Expected Output: 2 reservation objects, second reservation does get added
        """
        r = Room.objects.all()
        r.delete()
        room = create_room("130", "Rice Hall")
        create_room("125", "Minor Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)
        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Minor Hall', 'room_name': '125', 'start_time': '09:00', 'end_time': '10:00', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 2)

    def test_different_reservation_time(self):
        """
        Both reservations have same user, day, and room
        Reservation 1: 9:00 - 10:00
        Reservation 2: 10:00 - 9:00
        Expected Output: 2 reservation objects, second reservation does get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '10:00', 'end_time': '11:00', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 2)
        
    def test_same_reservation_time_different_day(self):
        """
        Both reservations have same user and room, but different day
        Reservation 1: 9:00 - 10:00
        Reservation 2: 9:00 - 10:00
        Expected Output: 2 reservation objects, second reservation does get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '09:00', 'end_time': '10:00', 'day': '2',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 2)
    
    def test_reservation_within_existing_reservation(self):
        """
        Both reservations have same user, day and room
        Reservation 1: 9:00 - 10:00
        Reservation 2: 9:15 - 9:45
        Expected Output: 1 reservation object, second reservation does not get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '09:15', 'end_time': '09:45', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 1)
    
    def test_reservation_subsumes_existing_reservation(self):
        """
        Both reservations have same user, day and room
        Reservation 1: 9:00 - 10:00
        Reservation 2: 8: - 11:00
        Expected Output: 1 reservation object, second reservation does not get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '08:00', 'end_time': '11:00', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 1)
        
    def test_reservation_endtime_within_existing_reservation(self):
        """
        Both reservations have same user, day and room
        Reservation 1: 9:00 - 10:00
        Reservation 2: 8:00 - 9:30
        Expected Output: 1 reservation object, second reservation does not get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '08:00', 'end_time': '09:30', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 1)
        
    def test_reservation_starttime_within_existing_reservation(self):
        """
        Both reservations have same user, day and room
        Reservation 1: 9:00 - 10:00
        Reservation 2: 9:30 - 11:00
        Expected Output: 1 reservation object, second reservation does not get added
        """
        room = create_room("130", "Rice Hall")
        user = create_user("Bob", "email@email.com", "Bobpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user, start_time=start, end_time=end, day=1)

        self.client.login(username="Bob", password="Bobpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '09:30', 'end_time': '11:00', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 1)

    def test_reservation_same_time_different_user(self):
        """
        Both reservations have same day and room, diff user
        Reservation 1: 9:00 - 10:00
        Reservation 2: 9:00 - 10:00
        Expected Output: 1 reservation object, second reservation does not get added
        """
        room = create_room("130", "Rice Hall")
        user1 = create_user("Bob", "email@email.com", "Bobpassword")
        create_user("Bill", "bill@emailcom", "Billpassword")
        start = datetime.datetime.strptime('09:00', '%H:%M').time()
        end = datetime.datetime.strptime('10:00', '%H:%M').time()
        Reservation.objects.create(title='Studying', room=room, user=user1, start_time=start, end_time=end, day=1)

        self.client.login(username="Bill", password="Billpassword")
        self.client.post(reverse('roomFinder_app:make_res'), data={
            'building': 'Rice Hall', 'room_name': '130', 'start_time': '09:30', 'end_time': '11:00', 'day': '1',
            'title': 'Project 1 meeting'
        })
        self.assertEqual(Reservation.objects.all().count(), 1)