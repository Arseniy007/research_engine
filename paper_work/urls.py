from django.urls import path
from . import views

app_name = "paper_work"

urlpatterns = [
    path("create_paper/<space_id>", views.create_paper, name="create_paper"),
    path("delete_paper/<int:paper_id>", views.delete_paper, name="delete_paper"),
    path("archive_paper/<int:paper_id>", views.archive_paper, name="archive_paper"),
    path("paper_space/<int:paper_id>", views.paper_space, name="paper_space"),
    path("rename_paper/<int:paper_id>", views.rename_paper, name="rename_paper"),
    path("publish_paper/<int:paper_id>", views.publish_paper, name="publish_paper"),
    path("select_sources/<int:paper_id>", views.select_sources_for_paper, name="select_sources")
]
