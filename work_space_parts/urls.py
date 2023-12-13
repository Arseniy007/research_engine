from django.urls import path
from . import views

app_name = "work_space_parts"

urlpatterns = [
    path("leave_comment/<int:space_id>", views.leave_comment, name="leave_comment"),
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("alter_comment/<int:comment_id>", views.alter_comment, name="alter_comment"),
    path("leave_note/<int:space_id>", views.leave_note, name="leave_note"),
    path("delete_note/<int:note_id>", views.delete_note, name="delete_note"),
    path("alter_note/<int:note_id>", views.alter_note, name="alter_note"),
    path("add_link/<int:space_id>", views.add_link, name="add_link"),
    path("delete_link/<int:link_id>", views.delete_link, name="delete_link"),
    path("alter_link/<int:link_id>", views.alter_link, name="alter_link")
]
