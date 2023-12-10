from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("index", views.index, name="index"),
    path("error_page", views.show_error_page, name="error_page")
]
