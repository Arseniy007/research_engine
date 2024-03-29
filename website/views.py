from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm, get_type_of_source_form
from citation.input_reference import create_input_reference
from utils.data_cleaning import clean_author_data
from utils.decorators import post_request_required
from utils.verification import check_invitation, check_share_sources_code
from user_management.helpers import get_user_papers, get_user_work_spaces
from work_space.forms import NewSpaceForm, ReceiveInvitationForm, ReceiveSourcesForm


def reference_view(request):
    """View for get-quick-reference-page"""

    data = {
        "book_form": BookForm(),
        "article_form": ArticleForm(),
        "chapter_form": ChapterForm(),
        "webpage_form": WebpageForm()
    }

    # About page if shown both for logged in and not logged in users
    if request.user.is_authenticated:
        data["work_spaces"] = get_user_work_spaces(request.user)
        data["papers"] = get_user_papers(request.user)

    return render(request, "website/reference.html", data)


@login_required(redirect_field_name=None)
def account_settings_view(request):
    """Main view for all settings"""

    data = {
        "work_spaces": get_user_work_spaces(request.user), 
        "papers": get_user_papers(request.user),
        "archived_spaces": get_user_work_spaces(request.user, archived=True),
        "archived_papers": get_user_papers(request.user, archived=True)
    }
    return render(request, "website/settings.html", data)


def invitation_view(request, code):
    """Render page with invitation to workspace or downloading sources"""

    # Check type of invitation and if it exists
    invitation_code = check_invitation(code)
    source_sharing_code = check_share_sources_code(code)

    # Figure out which of two codes it might be
    if invitation_code:
        data = {
            "invitation_form": ReceiveInvitationForm(), 
            "invitation_code": invitation_code.code, 
            "invitation": True
        }
    elif source_sharing_code:
        data = {
            "shared_sources_form": ReceiveSourcesForm(), 
            "share_sources_code": source_sharing_code.code, 
            "invitation": True
        }
    else:
        data = {}

    # Invitation page can be shown shown both for logged in and not logged in users
    if request.user.is_authenticated:
        data["work_spaces"] = get_user_work_spaces(request.user)
        data["papers"] = get_user_papers(request.user)

    return render(request, "website/invitation.html", data)


def about_view(request):
    """About page view"""

    # About page can be shown both for logged in and not logged in users
    if request.user.is_authenticated:
        data = {
            "work_spaces": get_user_work_spaces(request.user), 
            "papers": get_user_papers(request.user)
        }
    else:
        data = {}
    return render(request, "website/about.html", data)


@login_required(redirect_field_name=None)
def load_index_content(request):
    """API route for full-width sidenav"""

    data = {
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user),
        "new_space_form": NewSpaceForm(),
        "invitation_form": ReceiveInvitationForm(),
        "shared_sources_form": ReceiveSourcesForm()
    }
    return render(request, "website/index_content.html", data)


@post_request_required
def get_quick_reference(request):
    """Get reference for source that was inputted"""

    form = get_type_of_source_form(request.POST)
    if form and form.is_valid():
        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and isinstance(form, WebpageForm):
            # Error case
            pass
        else:
            if isinstance(form, ChapterForm):
                # Chapter is the only source type with two author fields
                chapter_author = clean_author_data(request.POST, chapter_author=True)
                if not chapter_author:
                    # Error case
                    pass
                else:
                    # Get reference for chapter
                    reference: dict | None = create_input_reference(form, author, chapter_author)
            else:
                # Get endnotes for all other types
                reference: dict | None = create_input_reference(form, author)
            if reference:
                return JsonResponse({"status": "ok", "reference": reference})

    # Error case
    return JsonResponse({"status": "error"})


def render_author_form_fields(request, author_number, chapter):
    """API route for getting author input fields for add-source-form"""
    # Chapter parameter is boolean (0/1). In case of True: pass "chapter-" as prefix to html tags
    if chapter:
        chapter = "chapter-"
    else:
        chapter = ""
    data = {
        "chapter": chapter,
        "author_number": author_number,
    }
    if request.user.is_authenticated:
        data["work_spaces"] = get_user_work_spaces(request.user)
        data["papers"] = get_user_papers(request.user)

    return render(request, "website/author_fields.html", data)
