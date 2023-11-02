from django.contrib import admin
from .models import Reservation, Room
from django.contrib.auth.models import Group

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fields=('room_name','room_location','capacity')


@admin.register(Reservation)
class EventAdmin(admin.ModelAdmin):
    fields = (('user','room','title'), 'start_time','end_time','day','created_at','approved')
    list_display = ('user','start_time','end_time','room')
    list_filter = ('start_time','end_time','room')
    order = ('start_time',)
    readonly_fields = ('created_at',)