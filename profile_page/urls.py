from django.urls import path
from . import views

app_name = "profile_page"

urlpatterns = [
    path("profile/<int:profile_id>", views.profile_page_view, name="profile_view"),
    path("follow/<int:profile_id>", views.follow_profile, name="follow_profile"),
    path("profile_settings/<int:profile_id>", views.profile_settings, name="profile_settings")
]
