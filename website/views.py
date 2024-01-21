from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm, get_type_of_source_form
from citation.input_reference import create_input_reference
from work_space.forms import NewSpaceForm, ReceiveCodeForm, ReceiveSourcesForm
from utils.data_cleaning import clean_author_data
from utils.decorators import post_request_required
from utils.messages import display_error_message, display_success_message
from user_management.helpers import get_user_papers, get_user_work_spaces


@login_required(redirect_field_name=None)
def index(request):

    data = {
        "form": NewSpaceForm(), 
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user),
        "invitation_form": ReceiveCodeForm(),
        "shared_sources_form": ReceiveSourcesForm()
    }
    return render(request, "website/index.html", data)


@login_required(redirect_field_name=None)
def load_index_content(request):
    """API route for full-width sidenav"""

    data = {
        "new_space_form": NewSpaceForm(),

    }
    return render(request, "website/index_navbar.html", data)


@login_required(redirect_field_name=None)
def account_settings_view(request):
    """Main view for all settings"""

    data = {
        "work_spaces": get_user_work_spaces(request.user), 
        "papers": get_user_papers(request.user)
    }
    return render(request, "website/account_settings.html", data)


def about_view(request):
    """About page view"""

    # About page if shown both for logged in and not logged in users
    if request.user.is_authenticated:
        data = {"work_spaces": get_user_work_spaces(request.user), "papers": get_user_papers(request.user)}
    else:
        data = {}
    return render(request, "website/about.html", data)


def lobby_view(request):
    """View for get-quick-reference-page"""

    # About page if shown both for logged in and not logged in users
    if request.user.is_authenticated:
        data = {"work_spaces": get_user_work_spaces(request.user), "papers": get_user_papers(request.user)}
    else:
        data = {}
    data["book_form"] = BookForm()
    data["article_form"] = ArticleForm()
    data["chapter_form"] = ChapterForm()
    data["webpage_form"] = WebpageForm()

    return render(request, "website/lobby.html", data)


@post_request_required
def get_quick_reference(request):
    """Get reference for source that was inputted"""

    form = get_type_of_source_form(request.POST)

    if form and form.is_valid():
        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            # Error case
            pass
        else:
            if type(form) == ChapterForm:
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
                reference: dict| None = create_input_reference(form, author)
            if reference:
                return JsonResponse({"status": "ok", "reference": reference})
            
    # Error case
    return JsonResponse({"status": "error"})


def render_author_form_fields(request, author_number, chapter):
    """API route for getting author input fields for add-source-form"""
    
    # Chapter parameter is boolean (0/1). In case of True: pass "chapter-" as prefix to html tag ids, classes and names
    if chapter:
       chapter = "chapter-"
    else:
        chapter = ""
    return render(request, "website/author_fields.html", {"author_number": author_number, "chapter": chapter})
