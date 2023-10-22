from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from .models import Room, User, Reservation



class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "room_list"

    def get_queryset(self):
        return Room.objects.all()
    
class RoomDetailView(generic.DetailView):
    model = Room
    template_name = "room_detail.html"
    
    def get_queryset(self):
        return Room.objects.all()
    
class ReservationCreate(generic.ListView):
    template_name = 'create_reservation.html'

    def get_queryset(self):
        return Reservation.objects.all()

"""
TODO
class ReservationDetailView(generic.DetailView):
    model = Reservation
    template_name = "reservation_detail.html"

    def get_queryset(self):
        return Reservation.object.all()
"""

"""
TODO
class UserDetailView(generic.DetailView):
    model = User
    template_name = "user_detail.html"

    show past bookings...
"""



