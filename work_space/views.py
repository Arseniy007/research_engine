import os
import shutil

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from bookshelf.forms import BookForm, ArticleForm, ChapterForm, WebsiteForm
from .forms import NewWorkSpaceForm, RenameWorkSpaceForm, ReceiveInvitationForm
from .friendly_dir import create_friendly_dir
from .invitation_generator import generate_invitation
from .models import WorkSpace
from paper_work.forms import NewPaperForm
from research_engine.settings import FRIENDLY_TMP_ROOT
from utils.decorators import space_ownership_required
from utils.verification import check_work_space, check_invitation


@login_required(redirect_field_name=None)
def index(request):

    return render(request, "work_space/index.html", {"form": NewWorkSpaceForm, 
                                                     "spaces": WorkSpace.objects.all(),
                                                     "form_invitation": ReceiveInvitationForm()})


@login_required(redirect_field_name=None)
def create_work_space(request):
    # TODO

    form = NewWorkSpaceForm(request.POST)

    if form.is_valid():
        # Save new work space to the db and create its directory
        new_space = form.save_work_space(request.user)
        new_space.create_dir()

        # Redirect user to the new work space
        link_to_work_space = reverse("work_space:space", args=(new_space.pk,))
        return redirect(link_to_work_space)

    # TODO
    print(form.errors)
    return redirect(reverse("user_management:error_page"))


@space_ownership_required
@login_required(redirect_field_name=None)
def delete_work_space(request, space_id):

    # Check if user has right to delete this work space
    space = check_work_space(space_id, request.user)

    # Delete work pace directory with all files inside
    shutil.rmtree(space.get_path())

    # Delete work s[ace] from the db
    space.delete()

    return JsonResponse({"message": "ok"})


@space_ownership_required
@login_required(redirect_field_name=None)
def archive_work_space(request, space_id):
    """Mark given work space as archived"""

    space = check_work_space(space_id, request.user)

    space.is_archived = True
    space.save(update_fields=("is_archived",))

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


@login_required(redirect_field_name=None)
def work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

   # author_formset = AuthorFormSet(prefix="author-formset")



    return render(request, "work_space/work_space.html", {"space": space, 
                                                          "papers": space.papers.all(),
                                                          "books": space.sources.all(),
                                                          "form": NewPaperForm(),
                                                          "book_form": BookForm(),
                                                          "article_form": ArticleForm(),
                                                          "chapter_form": ChapterForm(),
                                                          "website_form": WebsiteForm(),
                                                          })


def test(request):

    #AuthorFormSet = formset_factory(AuthorForm, formset="", can_delete=True, can_order=True)
    #author_formset = AuthorFormSet(prefix="author-formset")
    pass
    #return render(request, "work_space/test.html", {"author_formset": author_formset})


@space_ownership_required
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


@space_ownership_required
@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    """Create an invitation to work space for another user"""
    # TODO

    # Check if user has right to invite to the work space
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

        # Delete invitation code
        invitation.delete()

        link = reverse("work_space:space", args=(new_work_space.pk,))
        return redirect(link)

    else:
        print(form.errors)
        # TODO
        pass

    return JsonResponse({"message": "error"})


@login_required(redirect_field_name=None)
def leave_work_space(request, space_id):
    """Remove guest from a work space"""

    # Check if user was indeed a guest in a given work space
    space = check_work_space(space_id, request.user)
    if request.user not in space.guests.all():
        return JsonResponse({"message": "error"})

    # Remove user
    space.guests.remove(request.user)
    return JsonResponse({"message": "ok"})


@login_required(redirect_field_name=None)
def leave_comment(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)


@login_required(redirect_field_name=None)
def alter_comment(request, comment_id):
    # TODO

    pass


@login_required(redirect_field_name=None)
def delete_comment(request, comment_id):
    # TODO

    pass

    







# Is there a way to send request without forms in create and rename workspace functions?

# Comments? Each one has only one version of paper?
