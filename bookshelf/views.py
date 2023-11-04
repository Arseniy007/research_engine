from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewBookForm, AlterBookForm
from .models import Book
from utils.decorators import book_ownership_required
from utils.verification import check_book, check_work_space


@login_required(redirect_field_name=None)
def add_book(request, space_id):
    # TODO

    form = NewBookForm(request.POST, request.FILES)

    if form.is_valid():

        space = check_work_space(space_id, request.user)

        title = form.cleaned_data["title"]
        #author_last_name = form.cleaned_data["author_last_name"]
        #author_first_name = form.cleaned_data["author_first_name"]
        file = form.cleaned_data["file"]
        year, publishing_house = form.cleaned_data["year"], form.cleaned_data["publishing_house"]

        new_book = Book(user=request.user, work_space=space, title=title, author="s", year=year, publishing_house=publishing_house)
        new_book.save()
        new_book.file = file
        new_book.save(update_fields=("file",))

        link = reverse("work_space:space", args=(space.pk,))
        return redirect(link)
    
    else:
        print(form.errors)
        # TODO
        pass



@book_ownership_required
@login_required(redirect_field_name=None)
def delete_book(request, book_id):
    # TODO

    book = check_book(book_id, request.user)

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

    pass


