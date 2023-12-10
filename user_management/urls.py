from django.urls import path
from . import views

app_name = "user_management"

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("change_password", views.change_password, name="change_password")
]
