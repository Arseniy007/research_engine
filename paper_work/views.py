from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewPaperForm
from .models import Paper, PaperVersion
#from .paper_saving import save_paper, save_paper_version


@login_required(redirect_field_name=None)
def save_paper(request):
    # TODO

    form = NewPaperForm(request.POST, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():

            title = form.cleaned_data["title"]
            file = form.cleaned_data["file"]

            new_paper = Paper(user=request.user, title=title)
            new_paper.save()

            saved_paper = Paper.objects.get(user=request.user, title=title)

            new_version = PaperVersion(paper=saved_paper, user=request.user, file=file, paper_title=saved_paper.title)
            new_version.save()
        
        else:
            print(form.erros)


    return render(request, "paper_work/save_paper.html", {"form": form})

# need to have sepafate save version view
