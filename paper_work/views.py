from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import shutil

from .forms import NewPaperForm, RenamePaperForm
from file_handling.forms import NewPaperVersionForm
from .models import Paper
from file_handling.models import PaperVersion
from utils.verification import authorship_required, check_paper, check_work_space


@login_required(redirect_field_name=None)
def create_paper(request, space_id):
    """Adds new paper and creates a space for it"""
    
    form = NewPaperForm(request.POST)

    if form.is_valid():

        # Save new paper to db
        space = check_work_space(space_id, request.user)
        title = form.cleaned_data["title"]
        new_paper = Paper(work_space=space, user=request.user, title=title)
        new_paper.save()

        # Redirect user to the new paper-space
        saved_paper = Paper.objects.get(user=request.user, title=title)
        link = reverse("paper_work:paper_space", args=(saved_paper.pk,))
        return redirect(link)
        
    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))


@authorship_required
@login_required(redirect_field_name=None)
def delete_paper(request, paper_id):
    """Deletes added paper and all releted info"""

    # Check if user has right to delete this paper
    paper = check_paper(paper_id, request.user)
    
    # Delete paper directory with all files inside
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

    return render(request, "paper_work/paper_space.html", {"form": NewPaperVersionForm(), "paper": paper, "paper_versions": paper_versions, "links": links, "rename_form": RenamePaperForm()})


@authorship_required
@login_required(redirect_field_name=None)
def archive_paper(request, paper_id):
    """Mark paper is archived"""

    # Check if user has right to archive this paper
    paper = check_paper(paper_id, request.user)

    # Archive paper
    paper.is_archived = True
    paper.save(update_fields=("is_archive",))

    return JsonResponse({"message": "ok"})


@authorship_required
@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):

    form = RenamePaperForm(request.POST)

    if form.is_valid():

        paper = check_paper(paper_id, request.user)
        new_title = form.cleaned_data["new_title"]

        paper.title = new_title
        paper.save(update_fields=("title",))

        return JsonResponse({"message": "ok"})

    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))
        

@authorship_required
@login_required(redirect_field_name=None)
def finish_paper(request, paper_id):
    """Mark given paper as finished"""

    # Mark paper as finished
    paper = check_paper(paper_id, request.user)
    paper.is_finished = True
    paper.save(update_fields=("is_finished",))

    # Is that it?

    return JsonResponse({"message": "ok"})


@authorship_required
@login_required(redirect_field_name=None)
def publish_paper(request, paper_id):
    """Mark paper as published so it appers at the account page"""

    paper = check_paper(paper_id, request.user)

    if paper.is_finished:
        paper.is_published = True
        paper.save(update_fields=("is_published",))

        return JsonResponse({"message": "ok"})

    return JsonResponse({"message": "erro"})


@authorship_required
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
