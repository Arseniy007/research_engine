from django.urls import path

from . import views

app_name = "paper_work"

urlpatterns = [
    path("save_paper", views.save_paper, name="save_paper"),

]
