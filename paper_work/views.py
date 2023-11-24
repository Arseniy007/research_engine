import shutil
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import NewPaperForm, RenamePaperForm
from file_handling.forms import NewPaperVersionForm
from file_handling.models import PaperVersion
from .models import Paper
from utils.decorators import paper_authorship_required
from utils.verification import check_paper, check_work_space


@login_required(redirect_field_name=None)
def create_paper(request, space_id):
    """Adds new paper and creates a space for it"""
    
    form = NewPaperForm(request.POST)

    if form.is_valid():
        # Save new paper to db
        space = check_work_space(space_id, request.user)
        new_paper = form.save_paper(space, request.user)

        # Redirect user to the new paper-space
        link = reverse("paper_work:paper_space", args=(new_paper.pk,))
        return redirect(link)
        
    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))


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


@login_required(redirect_field_name=None)
def paper_space(request, paper_id):
    """Saves current version of the paper"""
    # TODO

    paper = check_paper(paper_id, request.user)

    paper_versions = PaperVersion.objects.filter(paper=paper).order_by("saving_time")

    links = [reverse("file_handling:display_file", args=(version.pk,)) for version in paper_versions]

    return render(request, "paper_work/paper_space.html", {"form": NewPaperVersionForm(), 
                                                           "paper": paper, "paper_versions": paper_versions, 
                                                           "links": links, "rename_form": RenamePaperForm()})


@paper_authorship_required
@login_required(redirect_field_name=None)
def archive_paper(request, paper_id):
    """Mark paper is archived"""

    # Check if user has right to archive this paper
    paper = check_paper(paper_id, request.user)

    # Archive paper
    paper.is_archived = True
    paper.save(update_fields=("is_archive",))

    return JsonResponse({"message": "ok"})


@paper_authorship_required
@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):

    form = RenamePaperForm(request.POST)

    if form.is_valid():
        # Update papers name
        paper = check_paper(paper_id, request.user)
        form.save_new_name(paper)

        return JsonResponse({"message": "ok"})

    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))
        

@paper_authorship_required
@login_required(redirect_field_name=None)
def finish_paper(request, paper_id):
    """Mark given paper as finished"""

    # Mark paper as finished
    paper = check_paper(paper_id, request.user)
    paper.is_finished = True
    paper.save(update_fields=("is_finished",))

    # Is that it?

    return JsonResponse({"message": "ok"})


@paper_authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):
    """Mark paper as published so it appers at the account page"""

    paper = check_paper(paper_id, request.user)

    if paper.is_finished:
        paper.is_published = True
        paper.save(update_fields=("is_published",))

        return JsonResponse({"message": "ok"})

    return JsonResponse({"message": "erro"})


@paper_authorship_required
@login_required(redirect_field_name=None)
def get_all_published_papers(request):
    """Return all papers marked as published to show display them at the account page"""

    papers = Paper.objects.filter(user=request.user, is_published=True)

    if not papers:
        return JsonResponse({"message": "none"})

    files = [paper.get_last_file_id() for paper in papers]
    # TODO
    pass



# What else?
