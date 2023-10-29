from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewWorkSpaceForm, RenameWorkSpaceForm, ReceiveInvitationForm
from .invitation_generator import generate_invitation
from .models import WorkSpace
from paper_work.forms import NewPaperForm
from utils.verification import check_work_space, check_invitation, ownership_required


@login_required(redirect_field_name=None)
def index(request):

    return render(request, "work_space/index.html", {"form": NewWorkSpaceForm, "spaces": WorkSpace.objects.all()})


@login_required(redirect_field_name=None)
def create_work_space(request):
    # TODO

    form = NewWorkSpaceForm(request.POST)

    if form.is_valid():

        # Save new work space to the db
        title = form.cleaned_data["title"]
        new_space = WorkSpace(owner=request.user, title=title)
        new_space.save()

        # Redirect user to the new work space
        new_space_id = WorkSpace.objects.get(owner=request.user, title=title).pk
        link_to_work_space = reverse("work_space:space", args=(new_space_id,))
        return redirect(link_to_work_space)

    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))


@ownership_required
@login_required(redirect_field_name=None)
def delete_work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    pass

@ownership_required
@login_required(redirect_field_name=None)
def archive_work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    # Archive work space
    space.is_archived = True
    space.save(update_fields=("is_archived",))

    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    return render(request, "work_space/work_space.html", {"space": space, "papers": space.papers.all(), "form": NewPaperForm()})


@ownership_required
@login_required(redirect_field_name=None)
def rename_work_space(request, space_id):
    # TODO

    form = RenameWorkSpaceForm(request.POST)

    if form.is_valid():

        space = check_work_space(space_id, request.user)

        new_title = form.cleaned_data["new_title"]
        space.title = new_title
        space.save(update_fields=("title",))

        return JsonResponse({"message": "ok"})

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})


@ownership_required
@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    invitation_code = generate_invitation(space)

    return JsonResponse({"invitation code": invitation_code})


@login_required(redirect_field_name=None)
def receive_invitation(request):
    '''Adds user as guest to the new work space if they were invited'''

    form = ReceiveInvitationForm(request.POST)

    if form.is_valid():

        # Check invitation code
        invitation_code = form.cleaned_data["code"]
        invitation = check_invitation(invitation_code)

        # Add user as guest to the new work space
        new_work_space = invitation.work_space
        new_work_space.guests.add(request.user)

        return JsonResponse({"message": "ok"})

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})


@login_required(redirect_field_name=None)
def leave_work_space(request, space_id):
    """Remove guest from a work space"""

    space = check_work_space(space_id, request.user)

    # Check if user was indeed a guest in a given work space
    if request.user not in space.guests.all():

        return JsonResponse({"message": "error"})

    # Remove user
    space.guests.remove(request.user)

    return JsonResponse({"message": "ok"})


# Is there a way to send request without forms in create and rename workspace functions

# Will there be any difference between s. adviser and co-author?
# Comments? Each one has only one version of paper?
