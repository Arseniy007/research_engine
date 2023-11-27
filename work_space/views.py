import os
import shutil
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from .forms import AlterCommentForm, CitationStyleForm, NewCommentForm, NewWorkSpaceForm, ReceiveInvitationForm, RenameWorkSpaceForm
from .friendly_dir import create_friendly_dir
from .invitation_generator import generate_invitation
from .models import WorkSpace
from paper_work.forms import NewPaperForm
from research_engine.settings import FRIENDLY_TMP_ROOT
from utils.decorators import comment_authorship_required, post_request_required, space_ownership_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_comment, check_invitation, check_work_space


@login_required(redirect_field_name=None)
def index(request):

    return render(request, "work_space/index.html", {"form": NewWorkSpaceForm(), 
                                                     "spaces": WorkSpace.objects.all(),
                                                     "form_invitation": ReceiveInvitationForm()})


@post_request_required
@login_required(redirect_field_name=None)
def create_work_space(request):
    """Create new worspace ;)"""

    form = NewWorkSpaceForm(request.POST)

    if form.is_valid():
        # Save new work space to the db and create its directory
        new_space = form.save_work_space(request.user)
        new_space.create_dir()
        display_success_message(request)

        # Redirect user to the new work space
        link_to_work_space = reverse("work_space:space", args=(new_space.pk,))
        return redirect(link_to_work_space)

    # TODO
    print(form.errors)
    display_error_message(request)
    return redirect(reverse("user_management:error_page"))


@space_ownership_required
@login_required(redirect_field_name=None)
def delete_work_space(request, space_id):

    # Check if user has right to delete this work space
    space = check_work_space(space_id, request.user)

    # Delete work pace directory with all files inside
    shutil.rmtree(space.get_path())

    # Delete workspace from the db
    space.delete()

    return JsonResponse({"message": "ok"})


@space_ownership_required
@login_required(redirect_field_name=None)
def archive_work_space(request, space_id):
    """Mark given work space as archived"""

    space = check_work_space(space_id, request.user)
    space.archive()
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def download_work_space(request, space_id):
    """Download archived (zip) file of the whole work space directory"""

    # Check if user has right to download the work space
    space = check_work_space(space_id, request.user)
    user_friendly_dir = create_friendly_dir(space)
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
def rename_work_space(request, space_id):
    """Allow workspace owner to rename space"""

    form = RenameWorkSpaceForm(request.POST)

    if form.is_valid():
        space = check_work_space(space_id, request.user)
        form.save_new_title(space)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("work_space:space", args=(space_id,))
    return redirect(link)


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
    
    link = reverse("work_space:space", args=(space_id,))
    return redirect(link)


@space_ownership_required
@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    """Create an invitation to work space for another user"""

    # TODO
    # Invitation text?

    # Check if user has right to invite to the work space
    space = check_work_space(space_id, request.user)
    invitation_code = generate_invitation(space)
    return JsonResponse({"invitation code": invitation_code})


@post_request_required
@login_required(redirect_field_name=None)
def receive_invitation(request):
    """Adds user as guest to the new work space if they were invited"""

    form = ReceiveInvitationForm(request.POST)

    if form.is_valid():
        # Check invitation code
        invitation_code = form.cleaned_data["code"]
        invitation = check_invitation(invitation_code)

        # Add user as guest to the new work space
        new_work_space = invitation.work_space
        new_work_space.add_guest(request.user)
        display_success_message(request)

        # Delete invitation code
        invitation.delete()
    else:
        display_error_message(request)

    link = reverse("work_space:space", args=(new_work_space.pk,))
    return redirect(link)



@login_required(redirect_field_name=None)
def leave_work_space(request, space_id):
    """Remove guest from a work space"""

    # Check if user was indeed a guest in a given work space
    space = check_work_space(space_id, request.user)
    if request.user not in space.guests.all():
        return JsonResponse({"message": "error"})

    # Remove user
    space.remove_guest(request.user)
    return JsonResponse({"message": "ok"})


@post_request_required
@login_required(redirect_field_name=None)
def leave_comment(request, space_id):
    """Leaves comment in given workspace"""

    form = NewCommentForm(request.POST)

    if form.is_valid():
        # Create new comment obj
        space = check_work_space(space_id, request.user)
        form.save_comment(space, request.user)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("work_space:space", args=(space.pk,))
    return redirect(link)


@comment_authorship_required
@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):
    """Deletes added comment"""

    # Check comment and if user has right to its deletion
    comment = check_comment(comment_id, request.user)

    # Delete comment from the db
    comment.delete()

    link = reverse("work_space:space", args=(comment.work_space.pk,))
    return redirect(link)


@post_request_required
@comment_authorship_required
@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):
    """Alter comment text"""

    form = AlterCommentForm(request.POST)

    if form.is_valid():
        comment = check_comment(comment_id, request.user)
        form.save_altered_comment(comment)
        display_success_message(request)
    else:
        display_error_message(request)

    link = reverse("work_space:space", args=(comment.work_space.pk,))
    return redirect(link)


@login_required(redirect_field_name=None)
def work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    return render(request, "work_space/work_space.html", {"space": space, 
                                                          "papers": space.papers.all(),
                                                          "books": space.sources.all(),
                                                          "form": NewPaperForm(),
                                                          "book_form": BookForm(),
                                                          "article_form": ArticleForm(),
                                                          "chapter_form": ChapterForm(),
                                                          "webpage_form": WebpageForm(),
                                                          "comment_form": NewCommentForm(),
                                                          "rename_form": RenameWorkSpaceForm().set_initial(space),
                                                          "citation_form": CitationStyleForm(),
                                                          "comments": space.comments.all()
                                                          })

@space_ownership_required
@login_required(redirect_field_name=None)
def share_sources(request):
    # TODO

    # or share workspace?
    # as a link?
    pass

# get all endnotes + get endnotes for the paper!
# add them automaticly to the end of the paper? - that would be nice!
