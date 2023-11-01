from django.urls import path

from . import views
from django.views.generic import TemplateView


app_name = "roomFinder_app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("map/", TemplateView.as_view(template_name="map.html"), name="map"),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("create/", views.make_reservation, name="create_reservation"),
]