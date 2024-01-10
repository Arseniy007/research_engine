import shutil
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.source_citation import get_endnotes
from .forms import CitationStyleForm, ChooseSourcesForm, NewPaperForm, RenamePaperForm
from file_handling.forms import UploadPaperFileForm
from file_handling.models import PaperFile
from profile_page.helpers import get_profile_id
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_paper, check_work_space


@login_required(redirect_field_name=None)
def paper_space(request, paper_id):
    """Main paper view"""
    
    paper = check_paper(paper_id, request.user)
    endnotes = [get_endnotes(source) for source in paper.sources.all()]
    paper_files = PaperFile.objects.filter(paper=paper).order_by("saving_time")
    links = [reverse("file_handling:display_paper_file", args=(file.pk,)) for file in paper_files]
    choose_sources_form = ChooseSourcesForm().set_initials(paper.work_space.sources.all())

    paper_data = {
        "paper": paper,
        "endnotes": endnotes,
        "paper_files": paper_files,
        "links": links,
        "choose_sources_form": choose_sources_form,
        "new_paper_file_form": UploadPaperFileForm(),
        "rename_paper_form": RenamePaperForm().set_initial(paper),
        "citation_form": CitationStyleForm()
    }
    return render(request, "paper_work/paper_space.html", paper_data)


@post_request_required
@login_required(redirect_field_name=None)
def create_paper(request, space_id):
    """Adds new paper and creates a space for it"""
    
    form = NewPaperForm(request.POST)

    if form.is_valid():
        # Save new paper to db
        space = check_work_space(space_id, request.user)
        new_paper = form.save_paper(space, request.user)
        display_success_message(request)

        # Redirect user to the new paper-space
        return JsonResponse({"status": "ok", "url": reverse("paper_work:paper_space", args=(new_paper.pk,))})
    
    display_error_message(request)
    return JsonResponse({"status": "error", "url": reverse("work_space:space_view", args=(space_id,))})


@paper_authorship_required
@login_required(redirect_field_name=None)
def delete_paper(request, paper_id):
    """Deletes added paper and all related info"""

    # Check if user has right to delete this paper
    paper = check_paper(paper_id, request.user)
    
    # Delete paper directory with all files inside
    if paper.files.all():
        shutil.rmtree(paper.get_path())

    # Delete paper from the db
    paper.delete()

    return JsonResponse({"message": "ok"})


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):
    """Change paper obj title"""

    form = RenamePaperForm(request.POST)

    if form and form.is_valid():
        # Update papers name
        paper = check_paper(paper_id, request.user)
        renamed_paper = form.save_new_name(paper)
        return JsonResponse({"status": "ok", "new_title": renamed_paper.title})
    
    # Send redirect url to js
    display_error_message(request)
    return JsonResponse({"url": reverse("paper_work:paper_space", args=(paper_id,))})


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def select_sources_for_paper(request, paper_id):
    """Allow user to choose from all sources in a work space to be used (cited) in a paper"""
    
    form = ChooseSourcesForm(request.POST)
    
    if form.is_valid():
        # Get all selected sources
        paper = check_paper(paper_id, request.user)
        selected_sources = form.cleaned_data["sources"]
        
        # Remove all sources that were not selected and add all chosen one
        for source in paper.sources.all():
            if source not in selected_sources:
                paper.sources.remove(source)
        paper.sources.add(*selected_sources)

        display_success_message(request)
    else:
        display_error_message(request)

    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def archive_or_unarchive_paper(request, paper_id):
    """Mark paper is archived or vice versa"""

    # Check if user has right to archive this paper
    paper = check_paper(paper_id, request.user)

    if paper.archived:
        paper.unarchive()
        # TODO
        # Redirect?
    else:
        paper.archive()
        # TODO
        # Redirect?

    display_success_message(request)
    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))
        

@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):
    """Mark paper as published so it appears at the account page"""

    # Check if user has right to publish this paper
    paper = check_paper(paper_id, request.user)

    # Check if paper file wsa uploaded
    if paper.get_number_of_files() != 0:
        # Publish paper
        paper.publish()
        display_success_message(request)
    else:
        display_error_message(request, "no files were uploaded")
        # TODO redirect back

    # Redirect to profile page
    return redirect(reverse("profile_page:profile_view", args=(get_profile_id(request.user),)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def hide_published_paper(request, paper_id):
    """Hide already published paper from users profile page"""

    # Check if user has right to hide this paper
    paper = check_paper(paper_id, request.user)

    # Error case
    if paper.published:
        # Mark paper as not published
        paper.unpublish()
        display_success_message(request)
    else:
        display_error_message(request)
        # TODO
        pass

    # TODO
    # Redirect back to profile page? Maybe Json would be better!
    return redirect(reverse("profile_page:profile_view", args=(get_profile_id(request.user),)))


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def set_citation_style(request, paper_id):
    """Choose citation style for all sources in work space"""
    
    form = CitationStyleForm(request.POST)

    if form.is_valid():
        paper = check_paper(paper_id, request.user)
        form.save_citation_style(paper)
        display_success_message(request)
    else:
        display_error_message(request)
    
    return redirect(reverse("work_space:space_view", args=(paper.work_space.pk,)))
