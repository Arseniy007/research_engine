import shutil
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.endnotes import get_endnotes
from .forms import ChooseSourcesForm, NewPaperForm, PaperPublicationForm, RenamePaperForm
from file_handling.forms import NewPaperVersionForm
from file_handling.models import PaperVersion
from profile_page.helpers import get_profile_id
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
    link = reverse("paper_work:paper_space", args=(paper_id,))
    return redirect(link)
        

@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):
    """Mark paper as published so it appers at the account page (or vice versa)"""

    form = PaperPublicationForm(request.POST)

    if form.is_valid():
        # Check if user has right to publish this paper
        paper = check_paper(paper_id, request.user)

        # Check if paper file wsa uploaded
        if paper.get_number_of_files() != 0:
            # Publish paper
            paper.publish()
    
            if form.cleaned_data["share_sources"]:
                # TODO ! What after?
                link = reverse("work_space:share_space", args=(paper.work_space.pk,))
                return redirect(link)
            
            display_success_message(request)
        else:
            display_error_message(request, "no files were uploaded")
    else:
        display_error_message(request)

    # Redirect to profile page
    profile_link = reverse("profile_page:profile_view", args=(get_profile_id(request.user),))
    return redirect(profile_link)


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
    profile_link = reverse("profile_page:profile_view", args=(get_profile_id(request.user),))
    return redirect(profile_link)


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
