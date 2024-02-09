from django.urls import path
from . import views

app_name = "work_space"

urlpatterns = [
    path("work_space/<int:space_id>", views.work_space_view, name="space_view"),
    path("create_work_space", views.create_work_space, name="create_space"),
    path("rename_space/<int:space_id>", views.rename_work_space, name="rename_space"),
    path("archive_space/<int:space_id>", views.archive_or_unarchive_space, name="archive_space"),
    path("download_space/<int:space_id>", views.download_work_space, name="download_space"),
    path("download_space_sources/<int:space_id>", views.download_space_sources, name="download_space_sources"),
    path("invite_to_space/<int:space_id>", views.invite_to_work_space, name="invite_to_space"),
    path("receive_invitation", views.receive_invitation, name="receive_invitation"),
    path("share_sources/<int:space_id>", views.share_space_sources, name="share_sources"),
    path("receive_shared_sources", views.receive_shared_sources, name="receive_shared_sources"),
    path("kick_member_out/<int:space_id>/<int:member_id>", views.kick_member_out_of_space, name="kick_member_out"),
    path("leave_space/<int:space_id>", views.leave_work_space, name="leave_space")
]
