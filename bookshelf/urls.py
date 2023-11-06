from django.urls import path

from . import views

app_name = "bookshelf"

urlpatterns = [
    path("add_book/<int:space_id>", views.add_book, name="add_book"),
    path("upload_book_file/<int:book_id>", views.upload_book_file, name="upload_book_file"),
    path("delete_book/<int:book_id>", views.delete_book, name="delete_book"),
    path("alter_book_info/<int:book_id>", views.alter_book_info, name="alter_book"),
    path("book_space/<int:book_id>", views.book_space, name="book_space"),
    path("add_quote/<int:book_id>", views.add_quote, name="add_quote"),
    path("delete_quote/<int:quote_id>", views.delete_quote, name="delete_quote"),
    path("alter_quote/<int:quote_id>", views.alter_quote, name="alter_quote")
]
