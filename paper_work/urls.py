from django.urls import path
from . import views

app_name = "paper_work"

urlpatterns = [
    path("paper_space/<int:paper_id>", views.paper_space, name="paper_space"),
    path("create_paper/<space_id>", views.create_paper, name="create_paper"),
    path("rename_paper/<int:paper_id>", views.rename_paper, name="rename_paper"),
    path("archive_paper/<int:paper_id>", views.archive_or_unarchive_paper, name="archive_paper"),
    path("select_sources/<int:paper_id>", views.select_sources_for_paper, name="select_sources"),
    path("transfer_paper/<int:paper_id>", views.transfer_paper_to_new_space, name="transfer_paper"),
    path("append_bibliography/<int:paper_id>", views.auto_append_bibliography, name="append_bibliography"),
    path("change_citation_style/<int:paper_id>", views.change_paper_citation_style, name="change_citation_style"),
    path("clear_paper_file_history/<int:paper_id>", views.clear_paper_file_history, name="clear_paper_file_history")
]
