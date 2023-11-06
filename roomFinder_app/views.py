from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.auth.models import User
from .models import Room, Reservation
from .forms import ReservationForm
from django.views.generic import CreateView
# from separate import room_generate
import datetime
import json
import pandas as pd
import requests
from datetime import timedelta,datetime
import re

def room_generate():
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term="

    # getting the term for url
    date = datetime.now()
    season = "2"
    if (date.month <= 12 and date.month >= 7):
        season = "8"
    term = "1" + str(date.year)[2:] + season


    # aggregating all valid page numbers to one object that has all json for current term classes
    index = 1
    request = requests.get(url + term + "&page=" + str(index))
    json_data = request.json()
    room_df = []
    while True:
        if not json_data:
            # print(index)
            break
    # making data frame of classes
        for c in json_data:
            if len(c['meetings'])>0:
                room = re.split('(\d+)', str(c['meetings'][0]['facility_descr']))
                start_time = c['meetings'][0]['start_time'][0:5]
                end_time = c['meetings'][0]['end_time'][0:5]
                start_date = c['meetings'][0]['start_dt']
                end_date = c['meetings'][0]['end_dt']
                if len(end_time)>1:
                    end = int(end_time[3:])
                    diff = 0
                    if end != 30 or end != 00:
                        if end < 30:
                            diff = 30 - end
                        else:
                            diff = 60 - end
                    time_object = datetime.strptime(end_time[0:5], '%H.%M')
                    minutes_add = timedelta(minutes=diff)
                    end_time = (time_object + minutes_add).time()
                if len(room) > 1:
                    room_name = room[0]
                    room_num = room[1]
                    arr = []
                    if "Mo" in c['meetings'][0]['days']:
                        room_df.append(["Monday", start_time, end_time,
                                        start_date, end_date, room_name.strip(),
                                        int(room_num)
                                        ])
                    if "Tu" in c['meetings'][0]['days']:
                        room_df.append(["Tuesday", start_time, end_time,
                                        start_date, end_date, room_name.strip(),
                                        int(room_num)
                                        ])
                    if "We" in c['meetings'][0]['days']:
                        room_df.append(["Wednesday", start_time, end_time,
                                        start_date, end_date, room_name.strip(),
                                        int(room_num)
                                        ])
                    if "Th" in c['meetings'][0]['days']:
                        room_df.append(["Thursday", start_time, end_time,
                                        start_date, end_date, room_name.strip(),
                                        int(room_num)
                                        ])
                    if "Fr" in c['meetings'][0]['days']:
                        room_df.append(["Friday", start_time, end_time,
                                        start_date, end_date, room_name.strip(),
                                        int(room_num)
                                        ])
        index += 1
        request = requests.get(url + term + "&page=" + str(index))
        json_data = request.json()


    room_df = pd.DataFrame(room_df)
    room_df.columns = ["Days", "Start_time", "End_time", "Start_date", "End_date", "Building", "Room"]
    room_df = room_df.sort_values(by=["Building", "Start_time"])
    return room_df

def import_data():
    df = room_generate()
    for index, row in df.iterrows():
        if not Room.objects.filter(room_id=row['Room'], building=row['Building']).exists():
            room = Room(room_id=row['Room'],building=row['Building'])
            room.save()
        reservation = Reservation(title='Class',room=room,user=User,start_time=row['Start_time'],
                                  end_time=row['End_time'],day=row['Days'])
        reservation.save()

class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "room_list"
    flag = 0
    if flag==0:
        import_data()
        flag=1

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
        room = Room.objects.all().get(room_id=room_name)
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
        room_object = Room.objects.all().get(room_id=room_name)
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



