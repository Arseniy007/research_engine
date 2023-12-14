from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .endnote_from_input import quote_input_source
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm, get_type_of_source_form
from utils.data_cleaning import clean_author_data
from utils.decorators import post_request_required
from utils.messages import display_error_message


def lobby_view(request):

    params = {
        "article_form": ArticleForm(),
        "book_form": BookForm(),
        "chapter_form": ChapterForm(),
        "webpage_form": WebpageForm()
    }

    return render(request, "lobby/lobby.html", params)


@post_request_required
def get_lobby_endnotes(request):
    """Get endnotes for source that was inputted"""

    form = get_type_of_source_form(request.POST)

    if form and form.is_valid():
        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            display_error_message(request)
        else:
            if type(form) == ChapterForm:
                # Chapter is the only source type with two author fields
                chapter_author = clean_author_data(request.POST, chapter_author=True)
                # Error case
                if not chapter_author:
                    display_error_message()
                else:
                    # Get endnotes for chapter
                    endnotes = quote_input_source(form, author, chapter_author)
            else:
                # Get endnotes for all other types
                endnotes = quote_input_source(form, author)
            if endnotes:
                return JsonResponse(endnotes)
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("lobby:view")})

 