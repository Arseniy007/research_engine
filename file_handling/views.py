from office_word_count import Counter
import shutil
import textract
from binascii import hexlify

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewPaperVersionForm
from .models import PaperVersion
from utils.decorators import paper_authorship_required
from utils.verification import check_paper, check_file


@login_required(redirect_field_name=None)
def upload_file(request, paper_id):
    """Upload .pdf/.docx file to the given paper"""

    form = NewPaperVersionForm(request.POST, request.FILES)

    if form.is_valid():

        # Get and save new file
        paper = check_paper(paper_id, request.user)
        new_version = PaperVersion(user=request.user, paper=paper, file=form.cleaned_data["file"])
        new_version.save()
        
    else:
        print(form.errors)
        # TODO
        return redirect(reverse("user_management:error_page"))

    return JsonResponse({"message": "ok"})


@paper_authorship_required
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
def display_file(request, file_id):

    # Get and chek file
    file = check_file(file_id, request.user)

    # Open and send it
    return FileResponse(open(file.get_full_path(), "rb"))


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


@paper_authorship_required
@login_required(redirect_field_name=None)
def clear_file_history(request, paper_id):
    """Delete all files related to given paper"""

    # Check if user has right to delete all files
    paper = check_paper(paper_id, request.user)

    # Delete paper directory with all files inside
    shutil.rmtree(paper.get_path())

    # Recreate new empty directory
    paper.create_directory()

    # Remove files from the db
    PaperVersion.objects.filter(paper=paper).delete()

    return JsonResponse({"message": "ok"})
