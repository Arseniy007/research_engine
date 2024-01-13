from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("index", views.index, name="index"),
    path("error_page", views.show_error_page, name="error_page"),
    path("lobby", views.lobby_view, name="lobby"),
    path("get_input_reference", views.get_input_reference, name="get_reference"),
    path("about", views.about_view, name="about")
]
