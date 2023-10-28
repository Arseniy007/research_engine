from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import shutil

from .forms import NewPaperForm, RenamePaperForm
from file_handling.forms import NewPaperVersionForm
from .models import Paper
from file_handling.models import PaperVersion
from utils.verification import authorship_required, check_paper


@login_required(redirect_field_name=None)
def create_paper(request):
    """Adds new paper and creates a space for it"""
    
    form = NewPaperForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            title = form.cleaned_data["title"]

            new_paper = Paper(user=request.user, title=title)
            new_paper.save()

            saved_paper = Paper.objects.get(user=request.user, title=title)

            link = reverse("paper_work:paper_space", args=(saved_paper.pk,))
            return redirect(link)
        
        else:
            print(form.errors)
            # TODO

    return render(request, "paper_work/create_paper.html", {"form": form})


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
def delete_paper(request, paper_id):
    """Deletes added paper and all releted info"""

    # Check if user has right to delete this paper
    paper = check_paper(paper_id, request.user)
    
    # Delete paper directory with all files inside
    shutil.rmtree(paper.get_path())

    # Delete paper from the db
    paper.delete()

    return JsonResponse({"message": "ok"})

@authorship_required
@login_required(redirect_field_name=None)
def archive_paper(request, paper_id):

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

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})

# What else?