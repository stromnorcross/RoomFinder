from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.auth.models import User
from .models import Room, Reservation
from .forms import ReservationForm
from django.views.generic import CreateView
from django.core.exceptions import ObjectDoesNotExist
# from separate import room_generate
import datetime
import json
import pandas as pd
import requests
from datetime import timedelta,datetime
import re

def dummy_user():
    try:
        return User.objects.get(username='class time')
    except ObjectDoesNotExist:
        print("Create a Dummy User")

def import_data():
    try:
        user = dummy_user()
        df = pd.read_csv("roomFinder_app/class_res.csv")
        for index, row in df.iterrows():
            if not Room.objects.filter(room_name=row['Room'], building=row['Building']).exists():
                room = Room(room_name=row['Room'],building=row['Building'])
                room.save()
            room = Room.objects.get(room_name=row['Room'],building=row['Building'])
            reservation = Reservation(title='Class',room=room,user=user,start_time=datetime.strptime(str(row['Start_time']), '%H.%M'),
                                      end_time=datetime.strptime(row['End_time'], '%H:%M:%S'),day=row['Days'])
            reservation.save()
    except IntegrityError:
        print("Create a Dummy User")

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "room_list"
    if Reservation.objects.count() < 6756:
        import_data()

    def get_queryset(self):
        return Room.objects.all()
    
class RoomDetailView(generic.DetailView):
    model = Room
    template_name = "room_detail.html"
    
    def get_queryset(self):
        return Room.objects.all()
    
# class ReservationCreate(generic.ListView):
#     template_name = 'create_reservation.html'
# 
#     def get_queryset(self):
#         return Reservation.objects.all()
# 
#     #@login_required(login_url='/user')

def make_reservation(request):
    if request.method == "POST":
        # change room_id for POST to be expected request
        room_name = request.POST['room_name']
        room = Room.objects.all().get(room_name=room_name)
        # for reservation in Reservation.objects.all().filter(room=room):
        # # only allow booking if the requested start time is after the reservation end time
        # # or requested end time is before reservation start time, need to check hotel reservation logic for if-elif
        #     if str(reservation.start_time) > request.POST['start_time'] and str(reservation.start_time) > request.POST['end_time']:
        #     # pass is a keyword that does nothing, kinda like break but instead it just lets the loop keep running to check
        #     # the requested start and end times with other reservations
        #         pass
        #     elif str(reservation.end_time) < request.POST['start_time'] and str(reservation.end_time) < request.POST['end_time']:
        #         pass
        #     else:
        #         #messages.warning(request, "Invalid Booking Time")
        #         #return redirect("homepage")

        current_user = request.user
        #booking_id = str(room_id) + str(datetime.datetime.now())
        reservation = Reservation()
        room_object = Room.objects.all().get(room_name=room_name)
        print(room_object)
        user_object = User.objects.all().get(username=current_user)
        print(user_object)
        reservation.user = user_object
        reservation.room = room_object
        reservation.title = request.POST['title']
        reservation.start_time = request.POST['start_time']
        reservation.end_time = request.POST['end_time']

        reservation.save()
        print(reservation)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    else:
        return HttpResponse('Access Denied')


def admin_delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.delete()
    return redirect("roomFinder_app:reservation_list")


class CreateResView(CreateView):
    form_class = ReservationForm
    template_name = "create_reservation.html"


class ReservationDetailView(generic.DetailView):
    model = Reservation
    template_name = "reservation_detail.html"

    def get_queryset(self):
        return Reservation.objects.all()
    
class ReservationListView(generic.ListView):
    #model = Reservation
    template_name = "reservation_list.html"
    context_object_name = "reservation_list"

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


"""
TODO

Inside the reservation detail view, there is a button to disapprove a reservation
def disapprove_res(request):


"""
"""
TODO
class UserDetailView(generic.DetailView):
    model = User
    template_name = "user_detail.html"

    show past bookings...
"""



