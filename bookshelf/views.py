import shutil
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .endnotes import get_endnotes
from .forms import *
from .source_alteration import alter_source
from .source_creation import create_source
from utils.data_cleaning import clean_author_data
from utils.decorators import endnote_ownership_required, quote_ownership_required, post_request_required, source_ownership_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_endnote, check_quote, check_source, check_work_space


@post_request_required
@login_required(redirect_field_name=None)
def add_source(request, space_id):
    """Add new source info to the work space"""
    # TODO
    # JS?

    form = get_type_of_source_form(request.POST)
    
    if form and form.is_valid():
        space = check_work_space(space_id, request.user)

        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            display_error_message(request)
        else:
            if type(form) == ChapterForm:
                chapter_author = clean_author_data(request.POST, chapter_author=True)
                if not chapter_author:
                    display_error_message()
                else:
                    create_source(request.user, space, form, author, chapter_author=chapter_author)
                    display_success_message(request)
            else:
                create_source(request.user, space, form, author)
                display_success_message(request)
    else:
        display_error_message()

    return redirect(reverse("work_space:space_view", args=(space.pk,)))
    

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


@post_request_required
@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_info(request, source_id):
    """Allow user to change all source related info"""

    form = get_type_of_source_form(request.POST, alter_source=True)

    if form and form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Alter and save source obj
        altered_source = alter_source(source, form)
        return JsonResponse({"status": "ok", "source": model_to_dict(altered_source)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@post_request_required
@login_required(redirect_field_name=None)
def upload_source_file(request, source_id):
    """Upload .pdf/.docx file of the given source"""

    form = UploadSourceForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        source = check_source(source_id, request.user)

        # In case user already uploaded a file - delete it first
        if source.file:
            shutil.rmtree(source.get_path())
        # Upload file
        source.file = request.FILES["file"]
        source.save(update_fields=("file",))
        display_success_message(request)
    else:
        display_error_message(request)

    # TODO
    return redirect(reverse("bookshelf:source_space", args=(source_id,)))


@login_required(redirect_field_name=None)
def display_source_file(request, source_id):

    # Get and check source
    source = check_source(source_id, request.user)

    source_file = source.get_path_to_file()
    if not source_file:
        display_error_message(request, "no file was uploaded")
        return redirect(reverse("bookshelf:source_space", args=(source_id,)))
    
    # Open source file and send it
    return FileResponse(open(source_file, "rb"))
    

@post_request_required
@login_required(redirect_field_name=None)
def add_link_to_source(request, source_id):
    """Adds link to a given source"""

    form = AddLinkForm(request.POST)

    if form and form.is_valid():
        source = check_source(source_id, request.user)
        added_link = form.save_link(source)
        if not added_link:
            return JsonResponse({"status": "error"})
        return JsonResponse({"status": "ok", "link": added_link})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@post_request_required
@endnote_ownership_required
@login_required(redirect_field_name=None)
def alter_endnote(request, source_id):
    """Alter endnote text"""

    form = AlterEndnoteForm(request.POST)
    source = check_source(source_id, request.user)
    endnote = get_endnotes(source)

    if form and form.is_valid():
        altered_endnote = form.save_altered_endnote(endnote)
        return JsonResponse({"status": "ok", "endnote": model_to_dict(altered_endnote)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@post_request_required
@login_required(redirect_field_name=None)
def add_quote(request, source_id):
    """Saves quote from given source"""

    form = NewQuoteForm(request.POST)

    if form and form.is_valid():
        source = check_source(source_id, request.user)
        new_quote = form.save_quote(source)
        return JsonResponse({"status": "ok", "quote": model_to_dict(new_quote)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(source_id,))})


@quote_ownership_required
@login_required(redirect_field_name=None)
def delete_quote(request, quote_id):
    """Delete added quote"""

    # Check quote and delete it from the db
    quote = check_quote(quote_id, request.user)
    quote.delete()
    return JsonResponse({"status": "ok"})


@post_request_required
@quote_ownership_required
@login_required(redirect_field_name=None)
def alter_quote(request, quote_id):
    """Alter quote text / page num."""

    form = AlterQuoteForm(request.POST)
    quote = check_quote(quote_id, request.user)

    if form and form.is_valid():
        altered_quote = form.save_altered_quote(quote)
        return JsonResponse({"status": "ok", "altered_quote": model_to_dict(altered_quote)})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(quote.source.pk,))})


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    # Delete later
    
    source = check_source(source_id, request.user)
    quotes = source.quotes.all()

    endnotes = get_endnotes(source)

    endnote_form = AlterEndnoteForm().set_initials(endnotes)

    upload_form = UploadSourceForm()
    quote_form = NewQuoteForm()
    link_form = AddLinkForm()

    alter_form = get_and_set_alter_form(source)
    
    return render(request, "bookshelf/source_space.html", {"source": source, 
                                                         "upload_form": upload_form, 
                                                         "alter_form": alter_form, 
                                                         "quote_form": quote_form,
                                                         "quotes": quotes,
                                                         "endnotes": endnotes,
                                                         "endnote_form": endnote_form,
                                                         "link_form": link_form})

# Alter messages text later!!!
