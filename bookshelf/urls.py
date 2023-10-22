from django.urls import path

from . import views

app_name = "bookshelf"

urlpatterns = [
    path("add_book", views.add_book, name="add_book"),
    path("delete_book_<int:book_id>", views.delete_book, name="delete_book"),
    path("save_paper", views.save_paper, name="save_paper")
]
