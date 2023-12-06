import shutil
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import ChooseSourcesForm, NewPaperForm, RenamePaperForm
from file_handling.forms import NewPaperVersionForm
from file_handling.models import PaperVersion
from utils.bridge import get_endnotes
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_paper, check_work_space


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
        link = reverse("paper_work:paper_space", args=(new_paper.pk,))
        return redirect(link)
    
    display_error_message(request)
    link_back = reverse("work_space:space_view", args=(space_id),)
    return redirect(link_back)
        

@paper_authorship_required
@login_required(redirect_field_name=None)
def delete_paper(request, paper_id):
    """Deletes added paper and all related info"""

    # Check if user has right to delete this paper
    paper = check_paper(paper_id, request.user)
    
    # Delete paper directory with all files inside
    if paper.versions.all():
        shutil.rmtree(paper.get_path())

    # Delete paper from the db
    paper.delete()

    return JsonResponse({"message": "ok"})


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):

    form = RenamePaperForm(request.POST)

    if form.is_valid():
        # Update papers name
        paper = check_paper(paper_id, request.user)
        form.save_new_name(paper)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("paper_work:paper_space", args=(paper_id,))
    return redirect(link)


@paper_authorship_required
@login_required(redirect_field_name=None)
def archive_paper(request, paper_id):
    """Mark paper is archived"""

    # Check if user has right to archive this paper
    paper = check_paper(paper_id, request.user)

    # Archive paper
    paper.archive()
    return JsonResponse({"message": "ok"})
        

@paper_authorship_required
@login_required(redirect_field_name=None)
def finish_paper(request, paper_id):
    """Mark given paper as finished"""

    # Mark paper as finished
    paper = check_paper(paper_id, request.user)
    paper.finish()

    # Do I need it?

    # Is that it?
    return JsonResponse({"message": "ok"})


@paper_authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):
    """Mark paper as published so it appers at the account page"""
    # TODO

    paper = check_paper(paper_id, request.user)

    if paper.is_finished:
        paper.publish()
        return JsonResponse({"message": "ok"})

    return JsonResponse({"message": "error"})


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
        
    link = reverse("paper_work:paper_space", args=(paper_id,))
    return redirect(link)


@login_required(redirect_field_name=None)
def paper_space(request, paper_id):
    """Saves current version of the paper"""
    # TODO

    # Delete later?

    paper = check_paper(paper_id, request.user)

    all_sources = paper.work_space.sources.all()

    sources_form = ChooseSourcesForm().set_initials(all_sources)

    paper_versions = PaperVersion.objects.filter(paper=paper).order_by("saving_time")

    endnotes = [get_endnotes(source) for source in paper.sources.all()]

    links = [reverse("file_handling:display_file", args=(version.pk,)) for version in paper_versions]

    # TODO

    return render(request, "paper_work/paper_space.html", {"form": NewPaperVersionForm(), 
                                                           "paper": paper, "paper_versions": paper_versions, 
                                                           "links": links, "rename_form": RenamePaperForm(),
                                                           "sources_form": sources_form,
                                                           "endnotes": endnotes})
# What else?
