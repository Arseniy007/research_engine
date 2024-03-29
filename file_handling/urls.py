from django.urls import path
from . import views

app_name = "file_handling"

urlpatterns = [
    path("upload_paper_file/<paper_id>", views.upload_paper_file, name="upload_paper_file"),
    path("delete_file/<int:file_id>", views.delete_paper_file, name="delete_paper_file"),
    path("paper_file/<int:file_id>", views.display_paper_file, name="display_paper_file"),
    path("paper_file_info/<int:file_id>", views.get_paper_file_info, name="paper_file_info"),
    path("upload_source_file/<int:source_id>", views.upload_source_file, name="upload_source_file"),
    path("source_file/<int:source_file_id>", views.display_source_file, name="display_source_file"),
]
