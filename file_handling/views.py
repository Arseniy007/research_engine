from binascii import hexlify
import shutil
import textract
from office_word_count import Counter
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from utils.decorators import paper_authorship_required, post_request_required
from utils.messages import display_error_message, display_info_message
from utils.verification import check_paper_file, check_paper, check_source, check_source_file
from .file_saving import save_new_paper_file, save_new_source_file
from .forms import UploadPaperFileForm, UploadSourceFileForm
from .page_counter import count_pages_docx, count_pages_pdf


@post_request_required
@login_required(redirect_field_name=None)
def upload_paper_file(request, paper_id):
    """Upload .pdf/.docx file to the given paper"""

    form = UploadPaperFileForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        paper = check_paper(paper_id, request.user)
        save_new_paper_file(
            paper, request.user,
            form.cleaned_data["file"],
            form.cleaned_data["commit_text"]
        )
        display_info_message(request, "File successfully uploaded!")
    else:
        display_error_message(request, "Something wrong with uploaded file. Try again!")

    return redirect(reverse("paper_work:paper_space", args=(paper_id,)))


@paper_authorship_required
@login_required(redirect_field_name=None)
def delete_paper_file(request, file_id):
    """:)"""
    # Get and check file
    file = check_paper_file(file_id, request.user)

    # Delete file directory with file inside
    shutil.rmtree(file.get_directory_path())

    # Delete file from the db
    file.delete()
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def display_paper_file(request, file_id):
    """:)"""
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
    file_data = Counter(decoded_text).count()

    # Count pages in .pdf file
    if file.file_extension == "pdf":
        number_of_pages = count_pages_pdf(file.get_path_to_file())

    # Count pages in .docx file
    elif file.file_extension == "docx":
        number_of_pages = count_pages_docx(file.get_path_to_file())

    response = {
        "number_of_words": file_data.words,
        "characters_no_space": file_data.characters_no_space,
        "characters_with_space": file_data.characters_with_space,
        "number_of_pages": number_of_pages
    }
    return JsonResponse(response)


@post_request_required
@login_required(redirect_field_name=None)
def upload_source_file(request, source_id):
    """Upload .pdf/.docx file of the given source"""

    form = UploadSourceFileForm(request.POST, request.FILES)

    if form.is_valid():
        # Get and save new file
        source = check_source(source_id, request.user)

        # In case user already uploaded a file - delete it first
        if source.has_file:
            shutil.rmtree(source.get_path())
            old_file = source.get_file()
            old_file.delete()
        save_new_source_file(source, form.cleaned_data["file"])
        display_info_message(request, "File successfully uploaded!")
    else:
        display_error_message(request, "Something wrong with uploaded file. Try again!")

    return redirect(reverse("bookshelf:source_space", args=(source_id,)))


@login_required(redirect_field_name=None)
def display_source_file(request, source_file_id):
    """:)"""
    # Get and check source
    file = check_source_file(source_file_id, request.user)

    # Open source file and send it
    return FileResponse(open(file.get_path_to_file(), "rb"))
