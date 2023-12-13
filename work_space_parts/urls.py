from django.urls import path
from . import views

app_name = "work_space_parts"

urlpatterns = [
    path("leave_comment/<int:space_id>", views.leave_comment, name="leave_comment"),
    path("delete_comment/<int:comment_id>", views.delete_comment, name="delete_comment"),
    path("alter_comment/<int:comment_id>", views.alter_comment, name="alter_comment")
]
