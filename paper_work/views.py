from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Paper


@login_required(redirect_field_name=None)
def save_paper(request):
    # TODO
    pass
