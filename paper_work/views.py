from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

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

            link = reverse("paper_work:save_paper", args=(saved_paper.pk,))
            return redirect(link)
        
        else:
            print(form.erros)
            # TODO

    return render(request, "paper_work/create_paper.html", {"form": form})


@login_required(redirect_field_name=None)
def save_paper(request, paper_id):
    """Saves current version of the paper"""

    paper = check_paper(request.user, paper_id)

    if not paper:
        # TODO 
        pass

    form = NewPaperVersionForm(request.POST, request.FILES or None)
    paper = Paper.objects.get(pk=paper_id)

    if request.method == "POST":

        if form.is_valid():

            file = form.cleaned_data["file"]

            new_version = PaperVersion(user=request.user, paper=paper, paper_title=paper.title, file=file)
            new_version.save()
            print(new_version)

        else:
            print(form.erros)
            # TODO
    
    paper_versions = PaperVersion.objects.filter(user=request.user, paper_title=paper.title).order_by("saving_date")

    links = [reverse("paper_work:show_file", args=(version.pk,)) for version in paper_versions]

    return render(request, "paper_work/save_paper.html", {"form": form, "paper": paper, "paper_versions": paper_versions, "links": links, "rename_form": RenamePaperForm()})


@login_required(redirect_field_name=None)
def delete_paper(request, paper_id):
    """Deletes added paper and all releted info"""

    paper = check_paper(request.user, paper_id)

    if not paper:
        # TODO 
        pass

    paper.delete()

    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def handle_file(request, file_id):

    file = check_file(request.user.pk, file_id)

    if not file:
        # TODO
        pass

    opened_file = open(file.get_path(), "rb")

    return FileResponse(opened_file)


@login_required(redirect_field_name=None)
def rename_paper(request, paper_id):

    paper = check_paper(request.user, paper_id)

    if not paper:
        # TODO 
        pass

    form = RenamePaperForm(request.POST)

    if form.is_valid():

        new_title = form.cleaned_data["new_title"]

        paper.title = new_title
        paper.save()
        return JsonResponse({"message": "ok"})

    else:
        print(form.errors)
        pass

    return JsonResponse({"message": "error"})