from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.db import IntegrityError
from django.views import generic
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Room, Reservation, Message, RoomRequest
from .forms import ReservationForm, RoomForm
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

def room_list(request, building_value):
    objects = Room.objects.all().filter(building=building_value, approved=True)
    return render(request, 'room_list.html', {'objects': objects, 'building_value': building_value})

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "building_list"
    if Reservation.objects.count() < 6756:
        import_data()

    def get_queryset(self):
        seen = set()
        uniqueBuildings = []
        for room in Room.objects.all().order_by('building'):
            if room.building not in seen and room.approved == True:
                seen.add(room.building)
                uniqueBuildings.append(room.building)
        return uniqueBuildings


class UnapprovedRoomsList(generic.ListView):
    template_name = "unapproved_rooms.html"
    context_object_name = "unapproved_rooms_list"

    def get_queryset(self):
        return Room.objects.filter(approved=False)

def approve_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.approved = True;
    room.save()
    return redirect("roomFinder_app:unapproved_rooms")

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room_req = RoomRequest.objects.filter(room=room).get()
    to_user = room_req.user
    message = Message()
    message.user = to_user
    message.message = str(room) + " does not exist at UVA. We deleted your request."
    message.title = "Regarding " + str(room)
    message.save()
    room.delete()
    return redirect("roomFinder_app:unapproved_rooms")

def delete_message(request, pk):
    message = get_object_or_404(Message, pk=pk)
    message.delete()
    return redirect("roomFinder_app:message_list")

class MessageListView(generic.ListView):
    template_name = "message_list.html"
    context_object_name = "message_list"

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(user=user).order_by('-pk')

class MessageDetailView(generic.DetailView):
    model = Message
    template_name = "message_detail.html"

    def get_queryset(self):
        return Message.objects.all()

class RoomDetailView(generic.DetailView):
    model = Room
    template_name = "room_detail.html"
    
    def get_queryset(self):
        return Room.objects.all()


class RoomListView(generic.ListView):
    template_name = "room_list.html"
    context_object_name = "room_list"

    def get_queryset(self):
        return Room.objects.all()

def add_room(request):
    if request.method == "POST":
        building = request.POST['building']
        room_name = request.POST['room_name']
        if building == "" or room_name == ""  or building.isspace() or room_name.isspace():
            messages.warning(request, "Please enter all information")
            return HttpResponseRedirect(reverse('roomFinder_app:add_new_room'))
        if Room.objects.filter(room_name=room_name, building=building).exists():
            messages.warning(request, "This room already exists")
            return HttpResponseRedirect(reverse('roomFinder_app:add_new_room'))
        room = Room()
        room.room_name = room_name
        room.building = building
        room.save()
        room_req = RoomRequest()
        current_user = request.user
        user_object = User.objects.all().get(username=current_user)
        room_req.user = user_object
        room_req.room = room
        room_req.save()
        messages.info(request, "Room submitted")

        return HttpResponseRedirect(reverse('roomFinder_app:add_new_room'))
    else:
        return HttpResponse('Access Denied')



def make_reservation(request):
    if request.method == "POST":
        try:
            if request.POST['title'] == "" or request.POST['title'].isspace():
                messages.warning(request, "Please enter a title.")
                return HttpResponseRedirect(reverse('roomFinder_app:create_reservation'))
            building = request.POST['building']
            room_name = request.POST['room_name']
            room = Room.objects.all().get(room_name=room_name, building=building)
            input_start_time = datetime.time(datetime.strptime(request.POST['start_time'], '%H:%M'))
            input_end_time = datetime.time(datetime.strptime(request.POST['end_time'], '%H:%M'))
            for reservation in Reservation.objects.all().filter(room=room):
                if not(reservation.day == request.POST['day']):
                    pass
                else:
                    if reservation.start_time > input_start_time and reservation.start_time >= input_end_time > input_start_time:
                        pass
                    elif reservation.end_time <= input_start_time < input_end_time and reservation.end_time < input_end_time:
                        pass
                    else:
                        messages.warning(request, "Invalid Booking Time: A Reservation Exists For This Time")
                        return HttpResponseRedirect(reverse('roomFinder_app:create_reservation'))

            current_user = request.user
            reservation = Reservation()
            room_object = Room.objects.all().get(room_name=room_name, building=building)
            print(room_object)
            user_object = User.objects.all().get(username=current_user)
            print(user_object)
            reservation.user = user_object
            reservation.room = room_object
            reservation.title = request.POST['title']
            reservation.start_time = request.POST['start_time']
            reservation.end_time = request.POST['end_time']
            reservation.day = request.POST['day']
            reservation.save()
            reservation_pk = reservation.pk
            reservation_detail_url = reverse('roomFinder_app:reservation_detail', args=[reservation_pk])
            return HttpResponseRedirect(reservation_detail_url)
        except ValueError:
            messages.warning(request, "Please enter a time")
            return HttpResponseRedirect(reverse('roomFinder_app:create_reservation'))
        except Room.DoesNotExist:
            messages.warning(request, "This room does not exist. Please pick a room that exists")
            return HttpResponseRedirect(reverse('roomFinder_app:create_reservation'))

    else:
        return HttpResponse('Access Denied')


def admin_delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.delete()
    return redirect("roomFinder_app:reservation_list")


class CreateResView(generic.ListView):
    #form_class = ReservationForm
    template_name = "create_reservation.html"
    context_object_name = "building_list"

    def get_queryset(self):
        seen = set()
        uniqueBuildings = []
        for room in Room.objects.all().order_by('building'):
            if room.building not in seen and room.approved == True:
                seen.add(room.building)
                uniqueBuildings.append(room.building)
        return uniqueBuildings

class AddRoomView(CreateView):
    form_class = RoomForm
    template_name = "add_new_room.html"

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
        user = self.request.user
        class_user = User.objects.get(username='class time')
        group_name = "admin"
        if user.groups.filter(name=group_name).exists():
            reservations = []
            for reservation in Reservation.objects.all().order_by("-created_at"):
                if reservation.user != class_user:
                    reservations.append(reservation)
            return reservations
        else:
            return Reservation.objects.filter(user=user).order_by("-created_at")


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



