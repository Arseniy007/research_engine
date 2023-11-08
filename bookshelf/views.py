import shutil

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewBookForm, UploadSourceForm, AlterSourceForm, NewQuoteForm
from utils.decorators import source_ownership_required, quote_ownership_required
from utils.verification import check_source, check_work_space, check_quote


@login_required(redirect_field_name=None)
def add_source(request, space_id):
    """Add new source info to the work space"""
    # TODO

    form = NewBookForm(request.POST)

    if form.is_valid():

        space = check_work_space(space_id, request.user)
        form.save_source(request.user, space)

        link = reverse("work_space:space", args=(space.pk,))
        return redirect(link)
    
    else:
        print(form.errors)
        # TODO
        pass


@login_required(redirect_field_name=None)
def upload_source_file(request, source_id):
    """Upload .pdf/.docx file of the given source"""

    form = UploadSourceForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        source = check_source(source_id, request.user)

        # In case user alrewedy uploaded a file - delete it first
        if source.file:
            shutil.rmtree(source.get_path())

        form.save_file(source)

        return JsonResponse({"message": "ok"})
    
    else:
        print(form.errors)
        # TODO
        pass


@source_ownership_required
@login_required(redirect_field_name=None)
def delete_source(request, source_id):
    """Deletes added source and all related info"""

    # Check if user has right to delete this paper
    source = check_source(source_id, request.user)

    # Delete paper directory with all files inside
    if source.file:
        shutil.rmtree(source.get_path())

    # Delete source from the db
    source.delete()

    return JsonResponse({"message": "ok"})


@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_info(request, source_id):
    """Allow user to change all source related info"""

    form = AlterSourceForm(request.POST)

    if form.is_valid():
        
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        form.save_source(source)

        link = reverse("sourceshelf:source_space", args=(source_id,))
        return redirect(link)

    else:
        print(form.errors)
        # TODO
        pass


@login_required(redirect_field_name=None)
def quote_sourse(request, source_id):
    # TODO

    source = check_source(source_id, request.user)
    # Do I need it?
    pass


@login_required(redirect_field_name=None)
def add_quote(request, source_id):
    """Saves quote from given source"""

    form = NewQuoteForm(request.POST)

    if form.is_valid():

        source = check_source(source_id, request.user)
        form.save_quote(source)

        link = reverse("bookshelf:source_space", args=(source_id,))
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

    link = reverse("bookshelf:source_space", args=(quote.source.pk,))
    return redirect(link)


@quote_ownership_required
@login_required(redirect_field_name=None)
def alter_quote(request, quote_id):

    pass


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    # Delete later

    source = check_source(source_id, request.user)
    quotes = source.quotes.all()

    upload_form = UploadSourceForm()
    quote_form = NewQuoteForm()
    alter_form = AlterSourceForm(initial={
                                        "title": source.title, 
                                        "author": source.author, 
                                        "year": source.year, 
                                        "publishing_house": "Test",
                                        })


    return render(request, "bookshelf/book_space.html", {"source": source, 
                                                         "upload_form": upload_form, 
                                                         "alter_form": alter_form, 
                                                         "quote_form": quote_form,
                                                         "quotes": quotes})
