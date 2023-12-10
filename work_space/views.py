import os
import shutil
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from .forms import CitationStyleForm, DeleteSpaceForm, NewSpaceForm, ReceiveCodeForm, RenameSpaceForm
from .friendly_dir import create_friendly_directory
from .invitation_generator import generate_invitation
from .models import WorkSpace
from paper_work.forms import NewPaperForm
from research_engine.settings import FRIENDLY_TMP_ROOT
from .space_creation import copy_space_with_all_sources, create_new_space
from utils.decorators import comment_authorship_required, post_request_required, space_ownership_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_comment, check_invitation, check_share_code, check_work_space
from work_comments.forms import AlterCommentForm, NewCommentForm


@login_required(redirect_field_name=None)
def index(request):

    return render(request, "work_space/index.html", {"form": NewSpaceForm(), 
                                                     "spaces": WorkSpace.objects.all(),
                                                     "invitation_form": ReceiveCodeForm(),
                                                     "shared_space_form": ReceiveCodeForm()})


@post_request_required
@login_required(redirect_field_name=None)
def create_work_space(request):
    """Create new worspace ;)"""

    form = NewSpaceForm(request.POST)

    if form.is_valid():
        # Save new work space to the db and create its directory
        new_space = create_new_space(request.user, form.cleaned_data["title"])
        display_success_message(request)

        # Redirect user to the new work space
        link_to_work_space = reverse("work_space:space_view", args=(new_space.pk,))
        return redirect(link_to_work_space)

    # TODO
    print(form.errors)
    display_error_message(request)
    return redirect(reverse("user_management:error_page"))


@post_request_required
@space_ownership_required
@login_required(redirect_field_name=None)
def delete_work_space(request, space_id):
    """Delete worspace ;)"""

    # TODO

    form = DeleteSpaceForm(request.POST)

    if form.is_valid():

        # Check if user has right to delete this work space
        space = check_work_space(space_id, request.user)

        # Delete work pace directory with all files inside
        shutil.rmtree(space.get_path())

        # Delete workspace from the db
        space.delete()

        return JsonResponse({"message": "ok"})
    
    # TODO
    # Return to index?
    return JsonResponse({"message": "error"})


@post_request_required
@space_ownership_required
@login_required(redirect_field_name=None)
def rename_work_space(request, space_id):
    """Allow workspace owner to rename space"""

    form = RenameSpaceForm(request.POST)

    if form.is_valid():
        space = check_work_space(space_id, request.user)
        form.save_new_title(space)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("work_space:space_view", args=(space_id,))
    return redirect(link)


@space_ownership_required
@login_required(redirect_field_name=None)
def archive_or_unarchive_space(request, space_id):
    """Mark given work space as archived"""

    space = check_work_space(space_id, request.user)

    if space.archived:
        space.unarchive()
    else:
        space.archive()
        # TODO
        # Redirect to index?

    # TODO
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def download_work_space(request, space_id):
    """Download archived (zip) file of the whole work space directory"""

    # Check if user has right to download the work space
    space = check_work_space(space_id, request.user)
    user_friendly_dir = create_friendly_directory(space)
    if not user_friendly_dir:
        # If work space is empry
        return JsonResponse({"message": "Empty Work Space"})

    # Create zip file of the directory
    saving_destination = os.path.join(space.get_friendly_path(), space.title)
    zip_file = shutil.make_archive(root_dir=user_friendly_dir, base_dir=space.title, base_name=saving_destination, format="zip")
    try:
        # Open and send it
        return FileResponse(open(zip_file, "rb"))
    finally:
        # Delete whole dir (with zip file inside)
        shutil.rmtree(FRIENDLY_TMP_ROOT)


@post_request_required
@space_ownership_required
@login_required(redirect_field_name=None)
def set_citation_style(request, space_id):
    """Choose citation style for all sources in work space"""
    
    form = CitationStyleForm(request.POST)

    if form.is_valid():
        space = check_work_space(space_id, request.user)
        form.save_citation_style(space)
        display_success_message(request)
    else:
        display_error_message(request)
    
    link = reverse("work_space:space_view", args=(space_id,))
    return redirect(link)


@space_ownership_required
@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    """Create an invitation to work space for another user"""
    # TODO
    # Invitation text?

    # Check if user has right to invite to the work space
    space = check_work_space(space_id, request.user)
    invitation_code = generate_invitation(space, invite=True)
    return JsonResponse({"invitation code": invitation_code})


@post_request_required
@login_required(redirect_field_name=None)
def receive_invitation(request):
    """Adds user as guest to the new work space if they were invited"""

    form = ReceiveCodeForm(request.POST)

    if form.is_valid():
        # Check invitation code
        invitation = check_invitation(form.cleaned_data["code"])

        # Add user as guest to the new work space
        new_work_space = invitation.work_space
        new_work_space.add_guest(request.user)
        display_success_message(request)

        # Delete invitation code
        invitation.delete()

        link = reverse("work_space:space_view", args=(new_work_space.pk,))
        return redirect(link)
    else:
        display_error_message(request)

    display_error_message(request)
    return redirect(reverse("user_management:error_page"))


@space_ownership_required
@login_required(redirect_field_name=None)
def share_work_space(request, space_id):
    """Share a copy of work space with all its sources"""
    # TODO

    # What should it be instead of json? probably url with some nice text

    space = check_work_space(space_id, request.user)
    if space.sources.all():
        share_space_code = generate_invitation(space)
        return JsonResponse({"share_space_code": share_space_code})
    else:
        return JsonResponse({"message": "You can not share empy work space"})


@post_request_required
@login_required(redirect_field_name=None)
def receive_shared_space(request):
    """Receive a copy of a work space with all its sources if it was shared"""
    # TODO

    form = ReceiveCodeForm(request.POST)

    if form.is_valid():
        share_space_code = check_share_code(form.cleaned_data["code"])

        # Create a new work space
        original_work_space = share_space_code.work_space
        new_space = copy_space_with_all_sources(original_work_space, request.user)

        # Redirect to the new work space
        display_success_message(request)
        link = reverse("work_space:space_view", args=(new_space.pk,))
        return redirect(link)

    display_error_message(request)
    return redirect(reverse("user_management:error_page"))


@login_required(redirect_field_name=None)
def leave_work_space(request, space_id):
    """Remove guest from a work space"""

    # Check if user was indeed a guest in a given work space
    space = check_work_space(space_id, request.user)

    # Error case
    if request.user not in space.guests.all():
        display_error_message(request)
        return_link = reverse("work_space:space_view", args=(space_id,))
        return redirect(return_link)

    # Remove user
    space.remove_guest(request.user)

    # TODO
    # Redirect to index?

    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def work_space_view(request, space_id):
    """Work space main view"""

    space = check_work_space(space_id, request.user)

    params = {"space": space, 
            "papers": space.papers.all(),
            "books": space.sources.all(),
            "form": NewPaperForm(),
            "book_form": BookForm(),
            "article_form": ArticleForm(),
            "chapter_form": ChapterForm(),
            "webpage_form": WebpageForm(),
            "comment_form": NewCommentForm(),
            "rename_form": RenameSpaceForm().set_initial(space),
            "citation_form": CitationStyleForm(),
            "comments": space.comments.all()
            }

    return render(request, "work_space/work_space_view.html", params)


# get all endnotes + get endnotes for the paper!
