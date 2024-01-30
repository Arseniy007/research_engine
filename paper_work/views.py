from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.source_citation import get_source_reference
from file_handling.forms import UploadPaperFileForm
from file_handling.models import PaperFile
from user_management.helpers import get_user_papers, get_user_work_spaces
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_paper, check_work_space
from .forms import ChooseSourcesForm, NewPaperForm, PaperSettingsForm


@login_required(redirect_field_name=None)
def paper_space(request, paper_id):
    """Main paper view"""
    
    # Get all needed paper-related data
    paper = check_paper(paper_id, request.user)
    endnotes = [get_source_reference(source) for source in paper.sources.all()]
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
        "settings_form": PaperSettingsForm().set_initial(paper),
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user)
    }
    return render(request, "paper_space.html", paper_data)


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


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def edit_paper_info(request, paper_id):
    """Change paper obj title"""

    form = PaperSettingsForm(request.POST)

    if form.is_valid():
        # Update paper info
        paper = check_paper(paper_id, request.user)



        
        form.save_changes(paper)



        display_success_message(request, "Paper info successfully updated!")

    else:
        # Error case
        display_error_message(request)

    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def archive_or_unarchive_paper(request, paper_id):
    """Mark paper is archived or vice versa"""

    # Check if user has right to archive this paper
    paper = check_paper(paper_id, request.user)

    if paper.archived:
        if paper.work_space.archived:
            # Error case
            error_message = f"{paper.title} is part of archived workspace: {paper.work_space.title}. You need to unarchive it first"
            display_error_message(request, error_message)
            return redirect(reverse("website:account_settings"))

        paper.unarchive()
        display_success_message(request, f"Paper is now again part of {paper.work_space.title} workspace!")
        return redirect(reverse("paper_work:paper_space", args=(paper_id,)))

    paper.archive()
    display_success_message(request, f"{paper.title} was successfully archived")
    return redirect(reverse("work_space:space_view", args=(paper.work_space.pk,)))


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def select_sources_for_paper(request, paper_id):
    """Allow user to choose from all sources in a work space to be used (cited) in a paper"""

    # TODO

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
