from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from work_space.forms import NewSpaceForm, ReceiveCodeForm
from work_space.models import WorkSpace
from utils.decorators import post_request_required, space_ownership_required
from utils.messages import display_error_message, display_success_message


@login_required(redirect_field_name=None)
def index(request):

    params = {"form": NewSpaceForm(), 
            "spaces": WorkSpace.objects.all(),
            "invitation_form": ReceiveCodeForm(),
            "shared_space_form": ReceiveCodeForm()}

    return render(request, "website/index.html", params)


def show_error_page(request):
    # TODO

    return render(request, "website/error_page.html")


