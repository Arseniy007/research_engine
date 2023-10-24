from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewPaperForm, NewPaperVersionForm
from .models import Paper, PaperVersion


@login_required(redirect_field_name=None)
def add_paper(request):
    

    form = NewPaperForm(request.POST, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():

            title = form.cleaned_data["title"]

            new_paper = Paper(user=request.user, title=title)
            new_paper.save()

            saved_paper = Paper.objects.get(user=request.user, title=title)

            link = reverse("paper_work:save_version", args=(saved_paper.pk,))
            return redirect(link)
        
        else:
            print(form.erros)


    return render(request, "paper_work/save_paper.html", {"form": form})


@login_required(redirect_field_name=None)
def save_paper(request, paper_id):
    """Saves current version of the paper"""

    form = NewPaperVersionForm(request.POST, request.FILES or None)
    paper = Paper.objects.get(pk=paper_id)

    if request.method == "POST":

        if form.is_valid():

            file = form.cleaned_data["file"]

            new_version = PaperVersion(user=request.user, paper=paper, paper_title=paper.title, file=file)
            new_version.save()

        else:
            print(form.erros)
            # TODO

    return render(request, "paper_work/save_version.html", {"form": form, "paper": paper})
