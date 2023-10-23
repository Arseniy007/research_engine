from django.urls import path

from . import views

app_name = "paper_work"

urlpatterns = [
    path("save_paper", views.save_paper, name="save_paper"),
    path("save_version/<int:paper_id>", views.save_paper_version, name="save_version")

]
