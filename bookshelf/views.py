import shutil
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .forms import *
from file_handling.forms import UploadSourceFileForm
from .source_alteration import alter_source
from .source_citation import get_source_reference
from .source_creation import create_source
from utils.data_cleaning import clean_author_data
from utils.decorators import quote_ownership_required, post_request_required, source_ownership_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_quote, check_source, check_work_space


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    """Main source view"""
    
    source = check_source(source_id, request.user)
    reference = get_source_reference(source)

    source_data = {
            "source": source,
            "quotes": source.quotes.all(),
            "reference": reference,
            "alter_source_form": get_and_set_alter_form(source),
            "upload_file_form": UploadSourceFileForm(),
            "link_form": AddLinkForm(),
            "new_quote_form": NewQuoteForm(),
            "alter_reference_form": AlterReferenceForm().set_initials(reference)
    }
    return render(request, "bookshelf/source_space.html", source_data)


@post_request_required
@login_required(redirect_field_name=None)
def add_source(request, space_id):
    """Add new source info to the work space"""
    
    # Figure out which of four forms was uploaded
    form = get_type_of_source_form(request.POST)
    
    if form and form.is_valid():
        space = check_work_space(space_id, request.user)

        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            # Error case
            pass
        else:
            if type(form) == ChapterForm:
                chapter_author = clean_author_data(request.POST, chapter_author=True)
                if not chapter_author:
                    # Error case
                    pass
                else:
                    display_success_message(request)
                    new_source_pk = create_source(request.user, space, form, author, chapter_author=chapter_author)
                    return JsonResponse({"status": "ok", "url": reverse("bookshelf:source_space", args=(new_source_pk,))})
            else:
                display_success_message(request)
                new_source_pk = create_source(request.user, space, form, author)
                return JsonResponse({"status": "ok", "url": reverse("bookshelf:source_space", args=(new_source_pk,))})
                        
    # Redirect back to work space
    display_error_message(request)
    return JsonResponse({"status": "error", "url": reverse("work_space:space_view", args=(space_id,))})


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
@source_ownership_required
@login_required(redirect_field_name=None)
def alter_source_reference(request, source_id):
    """Alter source reference text"""

    form = AlterReferenceForm(request.POST)
    source = check_source(source_id, request.user)
    reference = get_source_reference(source)

    if form and form.is_valid():
        altered_reference = form.save_altered_reference(reference)
        return JsonResponse({"status": "ok", "reference": model_to_dict(altered_reference)})

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
