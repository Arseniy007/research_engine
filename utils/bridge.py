from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from bookshelf.models import Endnote, Source
from profile_page.models import ProfilePage
from user_management.models import User


def get_profile_id(user: User) -> int | Http404:
    """Get profile id for given user"""
    try:
        return ProfilePage.objects.get(user=user).pk
    except ObjectDoesNotExist:
        raise Http404


def get_endnotes(source: Source) -> Endnote | Http404:
    """Get endnote for given source"""
    try:
        return Endnote.objects.get(source=source)
    except ObjectDoesNotExist:
        raise Http404
