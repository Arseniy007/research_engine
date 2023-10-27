from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import NewWorkSpaceForm, RenameWorkSpaceForm
from .models import WorkSpace, Invitation
from utils.verification import check_work_space


@login_required(redirect_field_name=None)
def index(request):


    return render(request, "work_space/index.html")


@login_required(redirect_field_name=None)
def create_work_space(request):
    # TODO

    form = NewWorkSpaceForm(request.POST or None)

    if form.is_valid():

        title = form.cleaned_data["title"]

        new_space = WorkSpace(owner=request.user, title=title)
        new_space.save()

        new_space_id = WorkSpace.objects.get(owner=request.user, title=title).pk

        link_to_work_space = reverse("work_space:space", args=(new_space_id,))

        redirect(link_to_work_space)


    else:
        print(form.errors)
        # TODO
        redirect(reverse("error_page.html"))


@login_required(redirect_field_name=None)
def archive_work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)

    pass


@login_required(redirect_field_name=None)
def work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)



    pass


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


@login_required(redirect_field_name=None)
def invite_to_work_space(request, space_id):
    # TODO

    space = check_work_space(space_id, request.user)


    pass


@login_required(redirect_field_name=None)
def receive_invitation(request):
    # TODO
    pass




# Is there a way to send request without forms in create and rename workspace functions
