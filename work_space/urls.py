from django.urls import path

from . import views

app_name = "work_space"

urlpatterns = [
    path("create_space", views.create_work_space, name="create_space"),
    path("delete_space/<int:space_id>", views.delete_work_space, name="delete_space"),
    path("archive_space/<int:space_id>", views.archive_work_space, name="archive_space"),
    path("work_space/<int:space_id>", views.work_space, name="space"),
    path("invite_to_space/<int:space_id>", views.invite_to_work_space, name="invite_to_space"),
    path("receive_invitation", views.receive_invitation, name="receive_invitation")
]
