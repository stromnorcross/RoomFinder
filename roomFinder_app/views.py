# *  REFERENCES
# *  ----------
# *  Title: Hotel-Room-Booking-System
# *  Author: SurajGuptaRavi
# *  Date: 2020
# *  URL: https://github.com/SurajGuptaRavi/Hotel-Room-Booking-System/blob/master/Krishna_Hotel/hotel/krishna/views.py
# *  used book_room function (lines 244-283) as a starting point for
# *  for our make_reservation function (lines 160-207)


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

building_coordinates = {'Astronomy Bldg': "38.035568, -78.515187", 'Biomed Engr & Med Sci': "38.030433, -78.499735", 'Bond House': "38.0293, -78.5041", 
                        'Brooks Hall': "38.035750, -78.502092", 'Brown Hall': "38.052923, -78.509306", 'Bryan Hall': "38.033263, -78.505940",
                        'Campbell Hall': "38.038724, -78.503845", 'Chemical Engineering Bldg': "38.033410, -78.510739", 'Chemistry Bldg': "38.033539, -78.511657",
                        'Clark Hall': "38.032998, -78.507857", 'Claude Moore Nursing Educ': "38.030769, -78.501686", 'Clemons Library': "38.036417, -78.506061",
                        'Cocke Hall': "38.033400, -78.505220", 'Collins Wing': "38.033348, -78.501611", 'Darden Classroom Bldg Room': "38.052551,-78.514637",
                        "Dawson's Row": "38.032250,-78.506411", 'Dell': "38.034913,-78.509954", 'Drama Education Bldg': "38.039623,-78.504383",
                        'Fayerweather Hall': "38.037815,-78.503079", 'French House': "38.031654,-78.502109", 'Gibson Hall': "38.031342,-78.505156",
                        'Gilmer Hall': "38.034132,-78.512746", 'Hunter Smith Band Building': "38.039856,-78.502925", 'Jesser Hall': "38.033120,-78.510882",
                        'John W. Warner Hall': "38.033378,-78.506791", 'Kerchof Hall': "38.032286,-78.508183", 'Lacy Room': "38.035640,-78.517774",
                        'Legal Aid Justice Center': "38.039149,-78.491610", 'Lower West Oval Room': "38.035704,-78.503531", 'Martha Jefferson Hospital CRN': "38.022735,-78.444283",
                        'McLeod Hall': "38.030881,-78.501646", 'Mechanical Engr Bldg': "38.032601,-78.511036", 'Memorial Gymnasium': "38.037373,-78.507181",
                        'Minor Hall': "38.033828,-78.506503", 'Monroe Hall': "38.034892,-78.506160", 'Multistory (Old) Hospital': "38.033270,-78.501137",
                        'Nau Hall': "38.031695,-78.504926", 'New Cabell Hall': "38.032540,-78.505108", 'Observ Mtn Eng Res Fac G': "38.041211,-78.521048",
                        'Old Cabell Hall': "38.032835,-78.504867", 'Olsson Hall': "38.031966,-78.510484", 'Pavilion V': "38.034970,-78.504193",
                        'Pavilion VIII': "38.034372,-78.503607", 'Physical & Life Sci Bldg Rm': "38.032850,-78.512241", 'Physics Bldg': "38.034252,-78.510244",
                        'PINN Hall': "38.031832,-78.500508", 'Randall Hall': "38.033251,-78.503314", 'Rice Hall': "38.031581,-78.510751",
                        'Ridley Hall': "38.034917,-78.509096", 'Robertson Hall': "38.032988,-78.503943", 'Rouss Hall': "38.032988,-78.503943",
                        'Ruffin Hall': "38.039320,-78.503173", 'Sands Captl Mgmt Bldg Rm': "38.052720,-78.514398", 'Shannon House': "38.033578,-78.514953",
                        'Slaughter Hall': "38.053259,-78.510573", 'Slaughter Rec': "38.034804,-78.517928", 'Student Health & Wellness': "38.030207,-78.503798",
                        'The Rotunda Room': "38.035594,-78.503352", 'Thornton Hall A': "38.033243,-78.509708", 'Thornton Hall D': "38.032905,-78.510245",
                        'Thornton Hall E': "38.032364,-78.510438", 'University Health Sciences': "38.031594,-78.500793", 'Wilsdorf Hall': "38.033303,-78.511243",
                        'Wilson Hall': "38.032455,-78.504022"} 

def room_list(request, building_value):
    objects = Room.objects.all().filter(building=building_value, approved=True)
    return render(request, 'room_list.html', {'objects': objects, 'building_value': building_value, 'building_coord': building_coordinates})

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
            #print(room_object)
            user_object = User.objects.all().get(username=current_user)
            #print(user_object)
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



