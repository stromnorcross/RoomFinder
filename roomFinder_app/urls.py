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
    path('reservation/delete/<int:pk>/', views.admin_delete_reservation, name='delete_reservation'),
]