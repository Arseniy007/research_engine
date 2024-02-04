import shutil
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from file_handling.forms import UploadSourceFileForm
from utils.data_cleaning import clean_author_data
from utils.decorators import quote_ownership_required, post_request_required, source_ownership_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_quote, check_source, check_work_space
from user_management.helpers import get_user_papers, get_user_work_spaces
from .forms import *
from .source_alteration import alter_source
from .source_citation import get_source_reference
from .source_creation import create_source
from .source_showcase import get_source_type


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    """Main source view"""

    source = check_source(source_id, request.user)
    reference = get_source_reference(source)

    if source.has_file:
        source_file_id = source.get_file().pk
    else:
        source_file_id = None

    # Get all needed source-related data
    source_data = {
            "source": source,
            "source_type": get_source_type(source),
            "reference": reference,
            "source_file_id": source_file_id,
            "quotes": source.quotes.all(),
            "alter_source_form": get_and_set_alter_form(source),
            "upload_file_form": UploadSourceFileForm(),
            "link_form": AddLinkForm().set_initials(source),
            "new_quote_form": NewQuoteForm(),
            "work_spaces": get_user_work_spaces(request.user), 
            "papers": get_user_papers(request.user)
    }
    return render(request, "source_space.html", source_data)


@post_request_required
@login_required(redirect_field_name=None)
def add_source(request, space_id):
    """Add new source info to the work space"""

    # Figure out which of four forms was uploaded
    form = get_type_of_source_form(request.POST)
    work_space_url = reverse("work_space:space_view", args=(space_id,))

    if form and form.is_valid():
        space = check_work_space(space_id, request.user)

        # Get and validate author(s) fields
        author = clean_author_data(request.POST)
        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            # Error case
            display_error_message(request, "Author fields should not be empty")
            return JsonResponse({"status": "error", "url": work_space_url})

        if type(form) == ChapterForm:
            chapter_author = clean_author_data(request.POST, chapter_author=True)
            if not chapter_author:
                # Error case
                pass
            else:
                # Success case with chapter form
                display_success_message(request)
                new_source_pk = create_source(request.user, space, form, author, chapter_author=chapter_author)
                return JsonResponse({"status": "ok", "url": reverse("bookshelf:source_space", args=(new_source_pk,))})
        else:
            # Success case with all other forms
            display_success_message(request)
            new_source_pk = create_source(request.user, space, form, author)
            return JsonResponse({"status": "ok", "url": reverse("bookshelf:source_space", args=(new_source_pk,))})
        
    print(form.errors)
                
    # Redirect back to work space
    display_error_message(request)
    return JsonResponse({"status": "error", "url": work_space_url})


@source_ownership_required
@login_required(redirect_field_name=None)
def delete_source(request, source_id):
    """Deletes added source and all related info"""

    # Check if user has right to delete this source
    source = check_source(source_id, request.user)

    # Delete paper directory with all files inside
    if source.has_file:
        shutil.rmtree(source.get_path())

    # Delete source from the db
    source.delete()
    return JsonResponse({"status": "ok"})


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
        alter_source(source, form)
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


@post_request_required
@login_required(redirect_field_name=None)
def add_link_to_source(request, source_id):
    """Adds link to a given source"""

    form = AddLinkForm(request.POST)

    if form and form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Add link
        form.save_link(source)
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


@post_request_required
@login_required(redirect_field_name=None)
def add_quote(request, source_id):
    """Saves quote from given source"""

    # TODO

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

    # TODO

    # Check quote and delete it from the db
    quote = check_quote(quote_id, request.user)
    quote.delete()
    return JsonResponse({"status": "ok"})


@post_request_required
@quote_ownership_required
@login_required(redirect_field_name=None)
def alter_quote(request, quote_id):
    """Alter quote text / page num."""

    # TODO

    form = AlterQuoteForm(request.POST)
    quote = check_quote(quote_id, request.user)

    if form and form.is_valid():
        altered_quote = form.save_altered_quote(quote)
        return JsonResponse({"status": "ok", "altered_quote": model_to_dict(altered_quote)})

    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("bookshelf:source_space", args=(quote.source.pk,))})
