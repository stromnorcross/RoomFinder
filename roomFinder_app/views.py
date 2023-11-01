from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic
from django.contrib.auth.models import User
from .models import Room, Reservation
from .forms import ReservationForm
from django.views.generic import CreateView



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
    
# class ReservationCreate(generic.ListView):
#     template_name = 'create_reservation.html'
# 
#     def get_queryset(self):
#         return Reservation.objects.all()
# 
#     #@login_required(login_url='/user')


class CreateResView(CreateView):
    form_class = ReservationForm
    template_name = "create_reservation.html"
    
    def make_reservation(self, request):
        if request.method == "POST":
            # change room_id for POST to be expected request
            room_name = request.POST['room_name']
            room = Room.objects.all().get(room_name=room_name)
            for reservation in Reservation.objects.all().filter(room=room):
            # only allow booking if the requested start time is after the reservation end time
            # or requested end time is before reservation start time, need to check hotel reservation logic for if-elif
                if str(reservation.start_time) > request.POST['start_time'] and str(reservation.start_time) > request.POST['end_time']:
                # pass is a keyword that does nothing, kinda like break but instead it just lets the loop keep running to check
                # the requested start and end times with other reservations
                    pass
                elif str(reservation.end_time) < request.POST['start_time'] and str(reservation.end_time) < request.POST['end_time']:
                    pass
                else:
                    messages.warning(request, "Invalid Booking Time")
                    return redirect("homepage")

            current_user = request.user
            #booking_id = str(room_id) + str(datetime.datetime.now())
            reservation = Reservation()
            room_object = Rooms.objects.all().get(room_name=room_name)
            user_object = User.objects.all().get(username=current_user)
            reservation.user = user_object
            reservation.room = room_object
            reservation.title = request.POST['title']
            reservation.start_time = request.POST['start_time']
            reservation.end_time = request.POST['end_time']

            reservation.save()

            return redirect("homepage")
        else:
            return HttpResponse('Access Denied')


class ReservationDetailView(generic.DetailView):
    model = Reservation
    template_name = "reservation_detail.html"

    def get_queryset(self):
        return Reservation.object.all()
    
class ReservationListView(generic.ListView):
    model = Reservation
    template_name = "reservation_list.html"

    def get_queryset(self):
        return Reservation.object.all()

"""
TODO
class UserDetailView(generic.DetailView):
    model = User
    template_name = "user_detail.html"

    show past bookings...
"""



