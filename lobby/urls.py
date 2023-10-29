from django.urls import path

from . import views

app_name = "lobby"

urlpatterns = [
    path("lobby", views.index, name="lobby"),
]
