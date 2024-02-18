import os
import shutil
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from bookshelf.forms import ArticleForm, BookForm, ChapterForm, WebpageForm
from paper_work.forms import NewPaperForm
from research_engine.constants import FRIENDLY_TMP_ROOT
from utils.decorators import post_request_required, space_ownership_required
from utils.messages import display_error_message, display_success_message
from utils.verification import check_invitation, check_share_sources_code, check_user, check_work_space
from user_management.helpers import get_user_papers, get_user_work_spaces
from .forms import NewSpaceForm, ReceiveInvitationForm, ReceiveSourcesForm, RenameSpaceForm
from .friendly_dir import create_friendly_sources_directory, create_friendly_space_directory
from .space_creation import copy_space_with_all_sources, create_new_space
from .space_sharing import generate_invitation, get_sources_sharing_code, share_sources
from .helpers import get_work_space_sources


@login_required
def work_space_view(request, space_id):
    """Work space main view"""

    # Get main data
    space = check_work_space(space_id, request.user)
    members = space.members.all()
    sources = get_work_space_sources(space)
    space_papers = space.papers.filter(archived=False)

    # Get all needed source-related data
    work_space_data = {
        "space": space,
        "sources": sources,
        "space_papers": space_papers,
        "owner": space.owner,
        "members": members,
        "user_status": space.get_user_status(request.user),
        "number_of_members": len(members) + 1, # 1 = Owner
        "space_has_sources": bool(sources),
        "number_of_sources": len(sources),
        "number_of_papers": len(space_papers),
        "new_paper_form": NewPaperForm(),
        "book_form": BookForm(),
        "article_form": ArticleForm(),
        "chapter_form": ChapterForm(),
        "webpage_form": WebpageForm(),
        "rename_form": RenameSpaceForm().set_initial(space.title),
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user),
    }
    return render(request, "work_space.html", work_space_data)


@post_request_required
@login_required(redirect_field_name=None)
def create_work_space(request):
    """Create new workspace ;)"""

    form = NewSpaceForm(request.POST)

    if form.is_valid():
        # Save new work space to the db and create its directory
        new_space_id = create_new_space(request.user, form.cleaned_data["title"]).pk

        # Redirect user to the new work space
        display_success_message(request)
        return JsonResponse({"status": "ok", "url": reverse("work_space:space_view", args=(new_space_id,))})

    # Error case
    return JsonResponse({"status": "error"})


@post_request_required
@space_ownership_required
@login_required(redirect_field_name=None)
def rename_work_space(request, space_id):
    """Allow workspace owner to rename space"""

    form = RenameSpaceForm(request.POST)

    if form.is_valid():
        # Update workspace title
        space = check_work_space(space_id, request.user)
        new_title = form.cleaned_data["title"]
        if new_title != space.title:
            space.title = new_title
            space.save(update_fields=("title",))
            display_success_message(request, "Workspace successfully renamed!")
    else:
        display_error_message(request)

    return redirect(reverse("work_space:space_view", args=(space_id,)))


@space_ownership_required
@login_required(redirect_field_name=None)
def archive_or_unarchive_space(request, space_id):
    """Mark given work space as archived"""

    space = check_work_space(space_id, request.user)

    if space.archived:
        # Mark workspace and all papers related to it as unarchived 
        space.unarchive()
        for paper in space.papers.all():
            paper.unarchive()

        display_success_message(request)
        return redirect(reverse("work_space:space_view", args=(space_id,)))

    # Mark workspace and all papers related to it as archived 
    space.archive()
    for paper in space.papers.all():
        paper.archive()

    display_success_message(request, f"{space.title} was successfully archived!")
    return redirect(reverse("website:account_settings"))


@login_required(redirect_field_name=None)
def download_work_space(request, space_id):
    """Download archived (zip) file of the whole work space directory"""

    # Check if user has right to download the work space
    space = check_work_space(space_id, request.user)
    user_friendly_dir = create_friendly_space_directory(space)
    if not user_friendly_dir:
        # If work space is empty
        return JsonResponse({"message": "Empty Work Space"})

    # Create zip file of the directory
    saving_destination = os.path.join(space.get_friendly_path(), space.title)
    zip_file = shutil.make_archive(root_dir=user_friendly_dir, base_dir=space.title, 
                                   base_name=saving_destination, format="zip")
    try:
        # Open and send it
        return FileResponse(open(zip_file, "rb"))
    finally:
        # Delete whole dir (with zip file inside)
        shutil.rmtree(FRIENDLY_TMP_ROOT)


@login_required(redirect_field_name=None)
def download_space_sources(request, space_id):
    """Download archived (zip) file with all space-related sources"""

    # Check if user has right to download the work space
    space = check_work_space(space_id, request.user)
    user_friendly_dir = create_friendly_sources_directory(space)
    if not user_friendly_dir:
        # If work space is empty
        return JsonResponse({"message": "Empty Work Space"})

    # Create zip file of the directory
    dir_title = "Sources"
    saving_destination = os.path.join(space.get_friendly_path(), dir_title)
    zip_file = shutil.make_archive(root_dir=user_friendly_dir, base_dir=dir_title, 
                                   base_name=saving_destination, format="zip")
    try:
        # Open and send it
        return FileResponse(open(zip_file, "rb"))
    finally:
        # Remove user from original space and delete whole dir (with zip file inside)
        space.remove_member(request.user)
        shutil.rmtree(FRIENDLY_TMP_ROOT)


@space_ownership_required
@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    """Create an invitation to work space for another user"""

    # Check if user has right to invite to the work space
    space = check_work_space(space_id, request.user)

    # Generate link with invitation code inside
    invitation_code = generate_invitation(space)
    invitation_link = request.build_absolute_uri(reverse("website:invitation", args=(invitation_code,)))
    return JsonResponse({"invitation_code": invitation_code, "invitation_link": invitation_link})


@space_ownership_required
@login_required(redirect_field_name=None)
def share_space_sources(request, space_id):
    """Share a copy of work space with all its sources"""

    # Check if user has right to share sources
    space = check_work_space(space_id, request.user)

    if space.sources.all():
        # Get source sharing link
        share_sources(space)
        share_sources_code = get_sources_sharing_code(space).code
        share_sources_link = request.build_absolute_uri(reverse("website:invitation", args=(share_sources_code,)))
        return JsonResponse({
            "status": "ok", 
            "sources_code": share_sources_code, 
            "sources_link": share_sources_link
        })
    # Error case
    return JsonResponse({"status": "error"})


@post_request_required
@login_required(redirect_field_name=None)
def receive_invitation(request):
    """Adds user as member to the new work space if they were invited"""

    form = ReceiveInvitationForm(request.POST)

    if form.is_valid():
        # Check invitation code
        invitation = check_invitation(form.cleaned_data["code"])

        if invitation:
            new_work_space = invitation.work_space

            work_space_url = reverse("work_space:space_view", args=(new_work_space.pk,))

            # Owner can't invite themselves and users who are already part of workspace
            if new_work_space.owner == request.user or request.user in new_work_space.members.all():
                return JsonResponse({
                    "status": "error", 
                    "message": f"{new_work_space} is your workspace", 
                    "url": work_space_url
                })
            # Add user as member to the new work space
            new_work_space.add_member(request.user)

            # Delete invitation code
            invitation.delete()

            # Send redirect to the new work space
            display_success_message(request)
            return JsonResponse({"status": "ok", "url": work_space_url})

    # Error case
    return JsonResponse({"status": "error", "message": "Something went wrong"})


@post_request_required
@login_required(redirect_field_name=None)
def receive_shared_sources(request):
    """Receive a copy of a work space with all its sources if it was shared"""

    form = ReceiveSourcesForm(request.POST)

    if form.is_valid():
        share_space_code = check_share_sources_code(form.cleaned_data["code"])
        if share_space_code:
            # Get original sources workspace
            original_work_space = share_space_code.work_space

            # Owner can't receive their own sources
            if original_work_space.owner == request.user or request.user in original_work_space.members.all():
                return JsonResponse({
                    "status": "error", 
                    "message": f"{original_work_space} is your workspace", 
                    "url": reverse("work_space:space_view", args=(original_work_space.pk,))
                })
            # Get one of two possible receiving options
            option = request.POST.get("option")
            if option == "create":
                # Create a new work space
                new_space = copy_space_with_all_sources(original_work_space, request.user)
                # Redirect to the new work space
                display_success_message(request)
                return JsonResponse({"status": "ok", "url": reverse("work_space:space_view", args=(new_space.pk,))})

            if option == "download":
                # Add user to space in order to download it and redirect them to download url
                original_work_space.add_member(request.user)
                download_url = reverse("work_space:download_space_sources", args=(original_work_space.pk,))
                return JsonResponse({"status": "ok", "url": download_url})

    # Error case
    return JsonResponse({"status": "error", "message": "Something went wrong"})


@space_ownership_required
@login_required(redirect_field_name=None)
def kick_member_out_of_space(request, space_id, member_id):
    """;)"""

    space, member = check_work_space(space_id, request.user), check_user(member_id)
    if member in space.members.all():
        # Remove member from workspace
        space.remove_member(member)
        display_success_message(request, f"{member} is no longer a part of {space}")
    # Error case
    else:
        display_error_message(request)
    return redirect(reverse("work_space:space_view", args=(space_id,)))


@login_required(redirect_field_name=None)
def leave_work_space(request, space_id):
    """Remove member from a work space"""

    # Check if user was indeed a member in a given work space
    space = check_work_space(space_id, request.user)

    # Error case
    if request.user not in space.members.all():
        display_error_message(request)
        return redirect(reverse("work_space:space_view", args=(space_id,)))

    # Remove user
    space.remove_member(request.user)

    # Redirect user to lobby page
    display_success_message(request)
    return redirect(reverse("website:lobby"))
