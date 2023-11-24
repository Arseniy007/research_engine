from django.urls import path
from . import views


app_name = "file_handling"

urlpatterns = [
    path("upload_file/<paper_id>", views.upload_file, name="upload_file"),
    path("delete_file/<int:file_id>", views.delete_file, name="delete_file"),
    path("file/<int:file_id>", views.display_file, name="display_file"),
    path("file_info/<int:file_id>", views.get_file_info, name="file_info"),
    path("clear_file_history/<int:paper_id>", views.clear_file_history, name="clear_history")
]
