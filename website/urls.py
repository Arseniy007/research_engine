from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("index", views.index, name="index"),
    path("error_page", views.show_error_page, name="error_page"),
    path("about", views.about_view, name="about"),
    path("lobby", views.lobby_view, name="lobby"),
    path("get_quick_reference", views.get_quick_reference, name="get_quick_reference"),
    path("render_author_field/<int:author_number>/<int:chapter>", views.render_author_form_fields, name="render_author_fields")
]
