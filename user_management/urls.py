from django.urls import path

from . import views

app_name = "user_management"

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("change_password", views.change_password, name="change_password"),
    path("error_page", views.show_error_page, name="error_page")
]
