from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.reference_view, name="quick_reference"),
    path("about", views.about_view, name="about"),
    path("index_content", views.load_index_content, name="index_content"),
    path("get_quick_reference", views.get_quick_reference, name="get_quick_reference"),
    path("account_settings", views.account_settings_view, name="account_settings"),
    path("invitation/<str:code>", views.invitation_view, name="invitation"),
    path("render_author_field/<int:author_number>/<int:chapter>", views.render_author_form_fields, name="render_author_fields")
]
