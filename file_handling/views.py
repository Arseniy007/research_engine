import shutil
import textract
from binascii import hexlify
from office_word_count import Counter
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from .forms import UploadPaperFileForm, UploadSourceFileForm
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_file, check_paper, check_source


@post_request_required
@login_required(redirect_field_name=None)
def upload_paper_file(request, paper_id):
    """Upload .pdf/.docx file to the given paper"""

    form = UploadPaperFileForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        paper = check_paper(paper_id, request.user)
        form.save_new_file(paper, request.user)
        display_success_message(request)
    else:
        display_error_message(request)

    # TODO Redirect where?
    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def delete_paper_file(request, file_id):

    # Get and check file
    file = check_file(file_id, request.user)

    # Delete file directory with file inside
    shutil.rmtree(file.get_directory_path())

    # Delete file from the db
    file.delete()
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def display_paper_file(request, file_id):

    # Get, check, open and send file
    file = check_file(file_id, request.user)
    return FileResponse(open(file.get_path_to_file(), "rb"))


@login_required(redirect_field_name=None)
def get_paper_file_info(request, file_id):
    """Returns info about text-file"""
    
    # Get, check and open file
    file = check_file(file_id, request.user)
    raw_text = textract.process(file.get_path_to_file())

    # Translate it into hexadecimal in order to handle different languages (äöü)
    hex_text = str(hexlify(raw_text))

    # Cut the unwanted part of the new string
    hex_text = hex_text[2:-1]

    # Decode text back from hexadecimal
    decoded_text = bytes.fromhex(hex_text).decode('utf-8')

    # Count words, characters, etc.
    info = Counter(decoded_text).count()

    response = {"number of words": info.words, 
                "characters with no space": info.characters_no_space,
                "characters with space": info.characters_with_space}
    
    return JsonResponse(response)


@paper_authorship_required
@login_required(redirect_field_name=None)
def clear_paper_file_history(request, paper_id):
    """Delete all files related to given paper"""

    # Check if user has right to delete all files
    paper = check_paper(paper_id, request.user)

    paper.clear_file_history()

    return JsonResponse({"message": "ok"})


@post_request_required
@login_required(redirect_field_name=None)
def upload_source_file(request, source_id):
    """Upload .pdf/.docx file of the given source"""

    form = UploadSourceFileForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        source = check_source(source_id, request.user)

        # In case user already uploaded a file - delete it first
        if source.file:
            shutil.rmtree(source.get_path())
        # Upload file
        source.file = request.FILES["file"]
        source.save(update_fields=("file",))
        display_success_message(request)
    else:
        display_error_message(request)

    # TODO
    return redirect(reverse("bookshelf:source_space", args=(source_id,)))


@login_required(redirect_field_name=None)
def display_source_file(request, source_id):

    # Get and check source
    source = check_source(source_id, request.user)

    source_file = source.file.get_path_to_file()
    if not source_file:
        display_error_message(request, "no file was uploaded")
        return redirect(reverse("bookshelf:source_space", args=(source_id,)))
    
    # Open source file and send it
    return FileResponse(open(source_file, "rb"))
