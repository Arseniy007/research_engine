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

    space = check_work_space(space_id, request.user)

    form = NewBookForm("#TODO")


    pass


@book_ownership_required
@login_required(redirect_field_name=None)
def delete_book(request, book_id):
    # TODO

    book = check_book(book_id, request.user)

    pass


@book_ownership_required
@login_required(redirect_field_name=None)
def alter_book_info(request, book_id):
    # TODO

    book = check_book(book_id, request.user)

    pass



@login_required(redirect_field_name=None)
def quote_book(request, book_id):
    # TODO

    book = check_book(book_id, request.user)

    pass


