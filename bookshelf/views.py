from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import shutil

from .forms import NewBookForm, UploadBookForm, AlterBookForm
from .models import Book
from utils.decorators import book_ownership_required
from utils.verification import check_book, check_work_space


@login_required(redirect_field_name=None)
def add_book(request, space_id):
    """Add new book info to the work space"""
    # TODO

    # deal with authors here!

    form = NewBookForm(request.POST)

    if form.is_valid():

        space = check_work_space(space_id, request.user)

        title = form.cleaned_data["title"]

        author_last_name = form.cleaned_data["author_last_name"]
        author_first_name = form.cleaned_data["author_first_name"]
        author_second_name = form.cleaned_data["author_second_name"]

        author = f"{author_last_name} {author_first_name} {author_second_name}"
        
        year, publishing_house = form.cleaned_data["year"], form.cleaned_data["publishing_house"]

        new_book = Book(user=request.user, work_space=space, title=title, author=author, year=year, publishing_house=publishing_house)
        new_book.save()

        link = reverse("work_space:space", args=(space.pk,))
        return redirect(link)
    
    else:
        print(form.errors)
        # TODO
        return JsonResponse({"message": "error"})
        pass


@login_required(redirect_field_name=None)
def upload_book(request, book_id):
    """Upload .pdf/.docx file of the given book"""

    form = UploadBookForm(request.POST, request.FILES)

    if form.is_valid():

        # Get and save new file
        book = check_book(book_id, request.user)
        book.file = form.cleaned_data["file"]
        book.save(update_fields=("file",))

        return JsonResponse({"message": "ok"})
        
    else:
        print(form.errors)
        # TODO
        pass


@book_ownership_required
@login_required(redirect_field_name=None)
def delete_book(request, book_id):
    """Deletes added book and all related info"""

    # Check if user has right to delete this paper
    book = check_book(book_id, request.user)

    # Delete paper directory with all files inside
    if book.file:
        shutil.rmtree(book.get_path())

    # Delete book from the db
    book.delete()

    return JsonResponse({"message": "ok"})


@book_ownership_required
@login_required(redirect_field_name=None)
def alter_book_info(request, book_id):
    # TODO

    book = check_book(book_id, request.user)

    form = AlterBookForm("#TODO")

    pass



@login_required(redirect_field_name=None)
def quote_book(request, book_id):
    # TODO

    book = check_book(book_id, request.user)

    # Do I need it?

    pass



@login_required(redirect_field_name=None)
def book_space(request, book_id):
    # Delete later

    book = check_book(book_id, request.user)

    form = UploadBookForm()

    return render(request, "bookshelf/book_space.html", {"book": book, "form": form})
