import shutil

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewBookForm, UploadBookForm, AlterBookForm, NewQuoteForm
from utils.decorators import book_ownership_required, quote_ownership_required
from utils.verification import check_book, check_work_space, check_quote


@login_required(redirect_field_name=None)
def add_book(request, space_id):
    """Add new book info to the work space"""
    # TODO

    form = NewBookForm(request.POST)

    if form.is_valid():

        space = check_work_space(space_id, request.user)
        form.save_form(request.user, space)

        link = reverse("work_space:space", args=(space.pk,))
        return redirect(link)
    
    else:
        print(form.errors)
        # TODO
        pass


@login_required(redirect_field_name=None)
def upload_book_file(request, book_id):
    """Upload .pdf/.docx file of the given book"""

    form = UploadBookForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        book = check_book(book_id, request.user)

        # In case user alredy uploaded a file - delete it first
        if book.file:
            shutil.rmtree(book.get_path())

        form.save_form(book)

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
    """Allow user to change all book related info"""

    form = AlterBookForm(request.POST)

    if form.is_valid():
        
        # Check book and get its attrs
        book = check_book(book_id, request.user)
        form.save_form(book)

        link = reverse("bookshelf:book_space", args=(book_id,))
        return redirect(link)

    else:
        print(form.errors)
        # TODO
        pass


@login_required(redirect_field_name=None)
def quote_book(request, book_id):
    # TODO

    book = check_book(book_id, request.user)
    # Do I need it?
    pass


@login_required(redirect_field_name=None)
def add_quote(request, book_id):
    """Saves quote from given book"""

    form = NewQuoteForm(request.POST)

    if form.is_valid():

        book = check_book(book_id, request.user)
        form.save_form(book)

        link = reverse("bookshelf:book_space", args=(book_id,))
        return redirect(link)

    else:
        print(form.errors)
        # TODO
        pass


@quote_ownership_required
@login_required(redirect_field_name=None)
def delete_quote(request, quote_id):
    """Delete added quote"""

    # Check quote and if user has right to deletion
    quote = check_quote(quote_id, request.user)

    # Delete quote from the db
    quote.delete()

    link = reverse("bookshelf:book_space", args=(quote.book.pk,))
    return redirect(link)


@quote_ownership_required
@login_required(redirect_field_name=None)
def alter_quote(request, quote_id):

    pass


@login_required(redirect_field_name=None)
def book_space(request, book_id):
    # Delete later

    book = check_book(book_id, request.user)
    quotes = book.quotes.all()

    upload_form = UploadBookForm()
    quote_form = NewQuoteForm()
    alter_form = AlterBookForm(initial={
                                        "title": book.title, 
                                        "author": book.author, 
                                        "year": book.year, 
                                        "publishing_house": book.publishing_house,
                                        })


    return render(request, "bookshelf/book_space.html", {"book": book, 
                                                         "upload_form": upload_form, 
                                                         "alter_form": alter_form, 
                                                         "quote_form": quote_form,
                                                         "quotes": quotes})
