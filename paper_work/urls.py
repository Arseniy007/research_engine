from django.urls import path

from . import views

app_name = "paper_work"

urlpatterns = [
    path("create_paper", views.create_paper_space, name="create_paper"),
    path("delete_paper/<int:paper_id>", views.delete_paper, name="delete_paper"),
    path("paper_space/<int:paper_id>", views.paper_space, name="paper_space"),
    path("rename_paper/<int:paper_id>", views.rename_paper, name="rename_paper"),
    path("file/<int:file_id>", views.display_file, name="display_file"),
    path("file_info/<int:file_id>", views.get_file_info, name="file_info"),
    path("delete_file/<int:file_id>", views.delete_file, name="delete_file"),
    path("clear_file_history/<int:paper_id>", views.clear_file_history, name="clear_history")
]
