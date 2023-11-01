from django.urls import path

from . import views


app_name = "roomFinder_app"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.RoomDetailView.as_view(), name="room_detail"),
    path("create/", views.make_reservation, name="create_reservation"),
]