from binascii import hexlify
import shutil
import textract
from office_word_count import Counter
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.urls import reverse
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message
from utils.verification import check_paper_file, check_paper, check_source, check_source_file
from .file_saving import save_new_paper_file, save_new_source_file
from .forms import UploadPaperFileForm, UploadSourceFileForm


@post_request_required
@login_required(redirect_field_name=None)
def upload_paper_file(request, paper_id):
    """Upload .pdf/.docx file to the given paper"""

    form = UploadPaperFileForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        paper = check_paper(paper_id, request.user)
        save_new_paper_file(form.cleaned_data["file"], paper, request.user)
        return JsonResponse({"status": "ok"})

    display_error_message(request, "Something wrong with uploaded file. Try again!")
    return JsonResponse({"url": reverse("paper_work:paper_space", args=(paper_id,))})


@paper_authorship_required
@login_required(redirect_field_name=None)
def delete_paper_file(request, file_id):

    # Get and check file
    file = check_paper_file(file_id, request.user)

    # Delete file directory with file inside
    shutil.rmtree(file.get_directory_path())

    # Delete file from the db
    file.delete()
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def display_paper_file(request, file_id):

    # Get, check, open and send file
    file = check_paper_file(file_id, request.user)
    return FileResponse(open(file.get_path_to_file(), "rb"))


@login_required(redirect_field_name=None)
def get_paper_file_info(request, file_id):
    """Returns info about text-file"""

    # Get, check and open file
    file = check_paper_file(file_id, request.user)
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

    return JsonResponse({"status": "ok"})


@post_request_required
@login_required(redirect_field_name=None)
def upload_source_file(request, source_id):
    """Upload .pdf/.docx file of the given source"""

    form = UploadSourceFileForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        source = check_source(source_id, request.user)

        if source.has_file:
            # In case user already uploaded a file - delete it first
            old_file = source.get_file()
            old_file.delete()
            shutil.rmtree(source.get_path())

        save_new_source_file(form.cleaned_data["file"], source)
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})


@login_required(redirect_field_name=None)
def display_source_file(request, source_file_id):

    # Get and check source
    file = check_source_file(source_file_id, request.user)

    # Open source file and send it
    return FileResponse(open(file.get_path_to_file(), "rb"))
