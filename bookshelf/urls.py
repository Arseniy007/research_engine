from django.urls import path

from . import views

app_name = "bookshelf"

urlpatterns = [
    path("add_book/<int:space_id>", views.add_book, name="add_book"),
    path("upload_book/<int:book_id>", views.upload_book, name="upload_book"),
    path("delete_book/<int:book_id>", views.delete_book, name="delete_book"),
    path("alter_book_info/<int:book_id>", views.alter_book_info, name="alter_book"),
    path("book_space/<int:book_id>", views.book_space, name="book_space")
]
