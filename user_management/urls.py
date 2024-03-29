from django.urls import path
from . import views

app_name = "user_management"

urlpatterns = [
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("edit_account_info", views.edit_account_info, name="edit_account"),
    path("change_password", views.change_password, name="change_password"),
    path("forget_password", views.forget_password, name="forget_password"),
    path("reset_password/<str:reset_code>", views.reset_password, name="reset_password")
]
