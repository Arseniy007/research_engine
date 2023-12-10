from django.urls import path

from . import views

app_name = "lobby"

urlpatterns = [
    path("lobby", views.lobby_view, name="view"),
    path("get_lobby_endnotes", views.get_lobby_endnotes, name="get_endnotes")
]
