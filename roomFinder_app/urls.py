from django.urls import path

from . import views
from django.views.generic import TemplateView


app_name = "roomFinder_app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("map/", TemplateView.as_view(template_name="map.html"), name="map"),
    path('room_list/<str:building_value>/', views.room_list, name='room_list'),
    path("room_list/<int:pk>/details/", views.RoomDetailView.as_view(), name="room_detail"),
    path("reservations/<int:pk>/details/", views.ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservations/", views.ReservationListView.as_view(), name="reservation_list"),
    path("create/", views.CreateResView.as_view(), name="create_reservation"),
    path("create/make_res", views.make_reservation, name="make_res"),
    path("add_new_room/", views.AddRoomView.as_view(), name="add_new_room"),
    path("add_new_room/add_room", views.add_room, name="add_room"),
    path("approve_rooms/", views.UnapprovedRoomsList.as_view(), name="unapproved_rooms"),
    path("room_list/<int:pk>/details/approve", views.approve_room, name="approve_room"),
    path("room_list/<int:pk>/details/delete", views.delete_room, name="delete_room"),
    path('reservation/<int:pk>/delete/', views.admin_delete_reservation, name='delete_reservation'),
]