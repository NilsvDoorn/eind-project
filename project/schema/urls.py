from django.urls import path

from . import views

urlpatterns = [
    path("", views.show_rooms, name="show_rooms"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("room_info", views.room_info, name="room_info"),
    path("cleanshifts", views.cleanshifts, name="cleanshifts"),
    path("reviews", views.reviews, name="reviews"),
    path("add_cleanshift", views.add_cleanshift, name="add_cleanshift"),
    path("add_review", views.add_review, name="add_review"),
    path("add_booking", views.add_booking, name="add_booking")
]
