from django.urls import path
from . import views

app_name = "work_space"

urlpatterns = [
    path("index", views.index, name="index"),
    path("create_space", views.create_work_space, name="create_space"),
    path("delete_space/<int:space_id>", views.delete_work_space, name="delete_space"),
    path("archive_space/<int:space_id>", views.archive_work_space, name="archive_space"),
    path("work_space/<int:space_id>", views.work_space, name="space"),
    path("rename_space/<int:space_id>", views.rename_work_space, name="rename_space"),
    path("invite_to_space/<int:space_id>", views.invite_to_work_space, name="invite_to_space"),
    path("receive_invitation", views.receive_invitation, name="receive_invitation"),
    path("leave_space/<int:space_id>", views.leave_work_space, name="leave_space"),
    path("download_space/<int:space_id>", views.download_work_space, name="download_space"),
    path("leave_comment/<int:space_id>", views.leave_comment, name="leave_comment"),
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("alter_comment/<int:comment_id>", views.alter_comment, name="alter_comment"),
    path("set_citation_style/<int:space_id>", views.set_citation_style, name="set_citation_style"),
    path("share_space/<int:space_id>", views.share_work_space, name="share_space"),
    path("receive_shared_space", views.receive_shared_space, name="receive_shared_space")
]
