from django.urls import path

from . import views
from django.views.generic import TemplateView


app_name = "roomFinder_app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("map/", TemplateView.as_view(template_name="map.html"), name="map"),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("<int:pk>/", views.ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservations/", views.ReservationListView.as_view(), name="reservation_list"),
    path("create/", views.CreateResView.as_view(), name="create_reservation"),
]