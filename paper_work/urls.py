from django.urls import path
from . import views

app_name = "paper_work"

urlpatterns = [
    path("paper_space/<int:paper_id>", views.paper_space, name="paper_space"),
    path("create_paper/<space_id>", views.create_paper, name="create_paper"),
    path("edit_paper/<int:paper_id>", views.edit_paper_info, name="paper_settings"),
    path("archive_paper/<int:paper_id>", views.archive_or_unarchive_paper, name="archive_paper"),
    path("select_sources/<int:paper_id>", views.select_sources_for_paper, name="select_sources")
]
