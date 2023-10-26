from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import shutil

from .forms import NewPaperForm, NewPaperVersionForm, RenamePaperForm
from .models import Paper, PaperVersion
from .verification import check_paper, check_file


@login_required(redirect_field_name=None)
def create_paper_space(request):
    """Adds new paper and creates a space for it"""
    
    form = NewPaperForm(request.POST, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():

            title = form.cleaned_data["title"]

            new_paper = Paper(user=request.user, title=title)
            new_paper.save()

            saved_paper = Paper.objects.get(user=request.user, title=title)

            link = reverse("paper_work:paper_space", args=(saved_paper.pk,))
            return redirect(link)
        
        else:
            print(form.erros)
            # TODO

    return render(request, "paper_work/create_paper.html", {"form": form})


@login_required(redirect_field_name=None)
def paper_space(request, paper_id):
    """Saves current version of the paper"""

    paper = check_paper(paper_id, request.user)

    form = NewPaperVersionForm(request.POST, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():

            file = form.cleaned_data["file"]

            new_version = PaperVersion(user=request.user, paper=paper, file=file)
            new_version.save()
            print(new_version)

        else:
            print(form.erros)
            # TODO
    
    paper_versions = PaperVersion.objects.filter(user=request.user, paper=paper).order_by("saving_date")

    links = [reverse("paper_work:show_file", args=(version.pk,)) for version in paper_versions]

    return render(request, "paper_work/paper_space.html", {"form": form, "paper": paper, "paper_versions": paper_versions, "links": links, "rename_form": RenamePaperForm()})


@login_required(redirect_field_name=None)
def delete_paper(request, paper_id):
    """Deletes added paper and all releted info"""

    # Check if user has right to delte this paper
    paper = check_paper(paper_id, request.user)
    
    # Delete paper directory with all files inside
    shutil.rmtree(paper.get_path())

    # Delete paper from the db
    paper.delete()

    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):

    paper = check_paper(paper_id, request.user)

    form = RenamePaperForm(request.POST)

    if form.is_valid():

        new_title = form.cleaned_data["new_title"]

        paper.title = new_title
        paper.save(update_fields=("title",))

        return JsonResponse({"message": "ok"})

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})


@login_required(redirect_field_name=None)
def display_file(request, file_id):

    file = check_file(file_id, request.user)

    return FileResponse(open(file.get_path(), "rb"))
