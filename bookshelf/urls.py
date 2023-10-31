from django.urls import path

from . import views

app_name = "bookshelf"

urlpatterns = [
    path("add_book/<int:space_id>", views.add_book, name="add_book"),
    path("delete_book_<int:book_id>", views.delete_book, name="delete_book"),
    path("alter_book_info/<int:book_id>", views.alter_book_info, name="alter_book")
]
