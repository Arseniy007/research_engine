from django.urls import path

from . import views

app_name = "paper_work"

urlpatterns = [
    path("add_paper", views.add_paper, name="add_paper"),
    path("save_paper/<int:paper_id>", views.save_paper, name="save_paper"),
    path("delete_paper/<int:paper_id>", views.delete_paper, name="delete_paper"),
    path("file/<int:file_id>", views.handle_file, name="show_file")
]
