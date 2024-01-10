from django.urls import path
from . import views

app_name = "bookshelf"

urlpatterns = [
    path("source_space/<int:source_id>", views.source_space, name="source_space"),
    path("add_source/<int:space_id>", views.add_source, name="add_source"),
    path("delete_source/<int:source_id>", views.delete_source, name="delete_source"),
    path("alter_source_info/<int:source_id>", views.alter_source_info, name="alter_source"),
    path("add_link_to_source/<int:source_id>", views.add_link_to_source, name="add_link"),
    path("alter_source_reference/<int:source_id>", views.alter_source_reference, name="alter_source_reference"),
    path("add_quote/<int:source_id>", views.add_quote, name="add_quote"),
    path("delete_quote/<int:quote_id>", views.delete_quote, name="delete_quote"),
    path("alter_quote/<int:quote_id>", views.alter_quote, name="alter_quote")
]
