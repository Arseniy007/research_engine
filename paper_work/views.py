from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from file_handling.forms import UploadPaperFileForm
from user_management.helpers import get_user_papers, get_user_work_spaces
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message, display_info_message, display_success_message
from utils.verification import check_paper, check_paper_file, check_work_space
from work_space.helpers import get_work_space_sources
from .bibliography import (
    append_bibliography_to_file, clear_bibliography, 
    get_right_bibliography, update_bibliography
)
from .forms import NewPaperForm, RenamePaperForm
from .helpers import (
    change_citation_style, create_new_paper, 
    get_chosen_source_ids, get_paper_files, rename_paper_obj
)


@login_required(redirect_field_name=None)
def paper_space(request, paper_id):
    """Main paper view"""

    # Get all needed paper-related data
    paper = check_paper(paper_id, request.user)
    sources = paper.sources.all()
    paper_files = get_paper_files(paper)

    paper_data = {
        "paper": paper,
        "paper_sources": sources,
        "paper_files": paper_files,
        "number_of_sources": len(sources),
        "number_of_files": len(paper_files),
        "last_file_id": paper.get_last_file_id(),
        "bibliography": get_right_bibliography(paper),
        "chosen_source_ids": get_chosen_source_ids(paper),
        "space_sources": get_work_space_sources(paper.work_space),
        "new_file_form": UploadPaperFileForm(),
        "rename_form": RenamePaperForm().set_initial(paper.title),
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
        # Get one of two possible citation styles
        citation_style = request.POST.get("citation_style")
        if citation_style in ("APA", "MLA",):
            # Save new paper to db
            new_paper = create_new_paper(
                check_work_space(space_id, request.user), 
                request.user, form.cleaned_data["title"], citation_style
            )
            display_success_message(request, "Paper successfully created")
            # Redirect user to the new paper-space
            return JsonResponse({"status": "ok", "url": reverse("paper_work:paper_space", args=(new_paper.pk,))})

    # Error case
    return JsonResponse({"status": "error"})


@post_request_required
@paper_authorship_required
@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):
    """Change paper obj title"""

    form = RenamePaperForm(request.POST)

    if form.is_valid():
        # Update paper title
        paper = check_paper(paper_id, request.user)
        new_title = form.cleaned_data["title"]
        if new_title != paper.title:
            rename_paper_obj(paper, new_title)
            display_success_message(request, "Paper successfully renamed!")
    else:
        # Error case
        display_error_message(request)

    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def change_paper_citation_style(request, paper_id):
    """Change paper citation style (APA / MLA)"""

    # Update paper info
    paper = check_paper(paper_id, request.user)
    citation_style = change_citation_style(paper)
    display_info_message(request, f"Citation style was set to {citation_style}")
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
        display_success_message(request, f" is now again part of {paper.work_space.title} workspace!")
        return redirect(reverse("paper_work:paper_space", args=(paper_id,)))

    paper.archive()
    display_success_message(request, f"{paper.title} was successfully archived")
    return redirect(reverse("work_space:space_view", args=(paper.work_space.pk,)))


@post_request_required
@login_required(redirect_field_name=None)
def select_sources_for_paper(request, paper_id):
    """Allow user to choose from all sources in a work space to be used (cited) in a paper"""

    # Get all selected sources
    paper = check_paper(paper_id, request.user)
    selected_sources = request.POST.getlist('sources-id')
    print(selected_sources)

    # Remove all sources that were not selected and add all chosen one
    for source in paper.sources.all():
        if source not in selected_sources:
            paper.sources.remove(source)
    paper.sources.add(*selected_sources)

    # Create new bibliography text
    update_bibliography(paper)

    # Redirect back to paper page
    display_info_message(request, "Bibliography updated!")
    return JsonResponse({"status": "ok", "url": reverse("paper_work:paper_space", args=(paper_id,))})


@paper_authorship_required
@login_required(redirect_field_name=None)
def auto_append_bibliography(request, paper_id):
    """Add bibliography to the end of a last uploaded file"""
    
    # Get last uploaded paper file
    paper = check_paper(paper_id, request.user)
    file = check_paper_file(paper.get_last_file_id(), request.user)

    # Choose between two citation styles
    append_bibliography_to_file(file, get_right_bibliography(paper))

    # Redirect to file_handling app to download .docx file
    return redirect(reverse("file_handling:display_paper_file", args=(file.pk,)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def clear_paper_file_history(request, paper_id):
    """Delete all files related to given paper"""

    # Check if user has right to delete all files
    paper = check_paper(paper_id, request.user)
    
    # Delete files and reset bibliography
    paper.clear_file_history()
    clear_bibliography(paper)
    display_info_message(request, "History cleared!")
    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))
