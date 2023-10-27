from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


@login_required(redirect_field_name=None)
def create_work_space(request):
    # TODO
    pass


@login_required(redirect_field_name=None)
def archive_work_space(request, space_id):
    # TODO
    pass


@login_required(redirect_field_name=None)
def rename_work_space(request, space_id):
    # TODO
    pass



@login_required(redirect_field_name=None)
def invite_to_work_space(request):
    # TODO
    pass


@login_required(redirect_field_name=None)
def receive_invitation(request):
    # TODO
    pass
