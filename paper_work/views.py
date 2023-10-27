from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from binascii import hexlify
from office_word_count import Counter
import shutil
import textract

from .forms import NewPaperForm, NewPaperVersionForm, RenamePaperForm
from .models import Paper, PaperVersion
from utils.verification import check_paper, check_file


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

    # Future upload_file function?

    paper = check_paper(paper_id, request.user)

    form = NewPaperVersionForm(request.POST, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():

            file = form.cleaned_data["file"]

            new_version = PaperVersion(paper=paper, file=file)
            new_version.save()
            print(new_version)

        else:
            print(form.erros)
            # TODO
    
    paper_versions = PaperVersion.objects.filter(paper=paper).order_by("saving_time")

    links = [reverse("paper_work:display_file", args=(version.pk,)) for version in paper_versions]

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

    # Get and chek file
    file = check_file(file_id, request.user)

    # Open and send it
    return FileResponse(open(file.get_full_path(), "rb"))


@login_required(redirect_field_name=None)
def delete_file(request, file_id):

    # Get and chek file
    file = check_file(file_id, request.user)

    # Delete file directory with file inside
    shutil.rmtree(file.get_directory_path())

    # Delete file from the db
    file.delete()

    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def get_file_info(request, file_id):
    """Returns info about text-file"""
    
    # Get, check and open file
    file = check_file(file_id, request.user)
    raw_text = textract.process(file.get_full_path())

    # Translate it into hexidesimal in order to handle different languages
    hex_text = str(hexlify(raw_text))

    # Cut the unwanted part of the new string
    hex_text = hex_text[2:-1]

    # Decode text back from hexidecimal
    decoded_text = bytes.fromhex(hex_text).decode('utf-8')

    # Count words, characters, etc.
    info = Counter(decoded_text).count()

    response = {"number of words": info.words, 
                "characters with no space": info.characters_no_space,
                "characters with space": info.characters_with_space}
    
    return JsonResponse(response)



# Send and receive invitations!
# Will there be any difference between s. adviser and co-author?
# Comments? Each one has only one version of paper?
# paper space viwe in paper_work???


# !!!!!!!

# Separate paper_space and all Paper class functions from files and PaperVersion function!
# Rewrite paper_space function!
