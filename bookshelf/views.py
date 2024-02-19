import shutil
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from citation.author_formatting import format_authors_apa
from file_handling.forms import UploadSourceFileForm
from utils.data_cleaning import clean_author_data
from utils.decorators import post_request_required, source_ownership_required
from utils.messages import display_error_message, display_info_message, display_success_message
from utils.verification import check_source, check_work_space
from user_management.helpers import get_user_papers, get_user_work_spaces
from .forms import (
    AddLinkForm, ChapterForm, WebpageForm, 
    get_and_set_alter_form, get_type_of_source_form
)
from .source_alteration import alter_source
from .source_citation import get_source_reference
from .source_creation import create_source


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    """Main source view"""

    source = check_source(source_id, request.user)
    reference = get_source_reference(source)
    source_header = f'"{source}" by {format_authors_apa(source.author)}'

    # Get all needed source-related data
    source_data = {
            "source": source,
            "reference": reference,
            "source_header": source_header,
            "source_type": source.get_type(),
            "source_file": source.get_file(),
            "alter_source_form": get_and_set_alter_form(source),
            "upload_file_form": UploadSourceFileForm(),
            "link_form": AddLinkForm().set_initials(source),
            "work_spaces": get_user_work_spaces(request.user), 
            "papers": get_user_papers(request.user)
    }
    return render(request, "main/source_space.html", source_data)


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
                
    # Redirect back to work space
    display_error_message(request)
    return JsonResponse({"status": "error", "url": work_space_url})


@source_ownership_required
@login_required(redirect_field_name=None)
def delete_source(request, source_id):
    """Deletes added source and all related info"""

    # Check if user has right to delete this source
    source = check_source(source_id, request.user)
    space_id = source.work_space.pk

    # Delete paper directory with all files inside
    if source.has_file:
        shutil.rmtree(source.get_path())

    # Delete source from the db
    source.delete()
    display_info_message(request, "Source successfully deleted!")
    return redirect(reverse("work_space:space_view", args=(space_id,)))


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
        display_info_message(request, "Info successfully updated!")
    else:
        display_error_message(request)
    return redirect(reverse("bookshelf:source_space", args=(source_id,)))
    

@post_request_required
@login_required(redirect_field_name=None)
def add_link_to_source(request, source_id):
    """Adds link to a given source"""

    form = AddLinkForm(request.POST)

    if form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Add link
        form.save_link(source)
        display_info_message(request, "Link successfully added!")
    else:
        display_error_message(request)
    return redirect(reverse("bookshelf:source_space", args=(source_id,)))
