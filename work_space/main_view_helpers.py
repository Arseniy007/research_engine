from django.http import Http404
from user_management.models import User
from .models import WorkSpace


def get_user_status(user: User, space: WorkSpace) -> str | Http404:
    """;)"""
    if user == space.owner:
        return "owner"
    elif user in space.guests.all():
        return "guest"
    else:
        raise Http404
