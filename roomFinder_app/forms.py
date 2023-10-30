from django.forms import ModelForm, inlineformset_factory
from django.contrib.auth.models import User
from .models import Reservation, Room


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['room_name', ]

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', ]


class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['title', 'room', 'user']


"""
TO-DO: form to add a reservation, reservation must connect to a room and user
ReservationFormSet = inlineformset_factory(Room, User, Reservation form=ReservationForm, extra=0, can_delete=False, min_num=1, validate_min=True,)
"""
