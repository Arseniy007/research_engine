import shutil
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import *
from .source_alteration import alter_source
from .source_creation import clean_author_data, create_source
from utils.decorators import source_ownership_required, quote_ownership_required, endnote_ownership_required
from utils.verification import check_source, check_work_space, check_quote, check_endnote, get_endnotes


@login_required(redirect_field_name=None)
def add_source(request, space_id):
    """Add new source info to the work space"""

    form = get_type_of_source_form(request.POST)
    if not form:
        return JsonResponse({"message": "error"})
    
    if form.is_valid():
        space = check_work_space(space_id, request.user)

        # Get and validate author(s) fields
        author = clean_author_data(request.POST)

        # Webpage is the only obj there author field could be blank
        if not author and type(form) != WebpageForm:
            # TODO
            return JsonResponse({"message": "error"})

        if type(form) == ChapterForm:
            chapter_author = clean_author_data(request.POST, chapter_author=True)
            if not chapter_author:
                # TODO
                return JsonResponse({"message": "error"})
            create_source(request.user, space, form, author, chapter_author=chapter_author)
        else:
            create_source(request.user, space, form, author)

        link = reverse("work_space:space", args=(space.pk,))
        return redirect(link)
    
    else:
        print(form.errors)
        # TODO
        return JsonResponse({"message": "error"})
    

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

    form = get_type_of_source_form(request.POST, alter_source=True)
    if not form:
        return JsonResponse({"message": "error"})

    if form.is_valid():
        # Check source and get its attrs
        source = check_source(source_id, request.user)
        # Alter and save source obj
        alter_source(source, form)

        link = reverse("bookshelf:source_space", args=(source_id,))
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


@login_required(redirect_field_name=None)
def add_link_to_source(request, source_id):
    """Adds link to a given source"""

    form = AddLinkForm(request.POST)

    if form.is_valid():
        source = check_source(source_id, request.user)
        if not form.save_link(source):
            return JsonResponse({"message": "error"})
        return JsonResponse({"message": "ok"})
    
    else:
        print(form.errors)
        # TODO
        pass


@endnote_ownership_required
@login_required(redirect_field_name=None)
def alter_endnote(request, endnote_id):
    """Alter endnote text"""

    form = AlterEndnoteForm(request.POST)

    if form.is_valid():
        endnote = check_endnote(endnote_id, request.user)
        form.save_endnote(endnote)

        source = check_source(endnote.source.pk, request.user)
        link = reverse("bookshelf:source_space", args=(source.pk,))
        return redirect(link)

        # TODO

    else:
        print(form.errors)
        # TODO
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

    # Check quote and if user has right to its deletion
    quote = check_quote(quote_id, request.user)
    
    # Delete quote from the db
    quote.delete()

    link = reverse("bookshelf:source_space", args=(quote.source.pk,))
    return redirect(link)


@quote_ownership_required
@login_required(redirect_field_name=None)
def alter_quote(request, quote_id):
    """Alter quote text / page num."""

    form = AlterQuoteForm(request.POST)

    if form.is_valid():
        quote = check_quote(quote_id, request.user)
        form.save_altered_quote(quote)

        link = reverse("bookshelf:source_space", args=(quote.source.pk,))
        return redirect(link)
    
    else:
        print(form.errors)
        # TODO
        pass


@login_required(redirect_field_name=None)
def source_space(request, source_id):
    # Delete later

    source = check_source(source_id, request.user)
    quotes = source.quotes.all()

    endnotes = get_endnotes(source)

    endnote_form = AlterEndnoteForm(initial={"apa": endnotes.apa, "mla": endnotes.mla})

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
