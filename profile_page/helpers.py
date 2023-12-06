from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from paper_work.models import Paper
from profile_page.models import ProfilePage
from user_management.models import User


def get_profile_id(user: User) -> int | Http404:
    """Get profile id for given user"""
    try:
        return ProfilePage.objects.get(user=user).pk
    except ObjectDoesNotExist:
        raise Http404


def get_all_published_papers(user: User) -> list | None:
    """Get all papers marked as published for given user"""
    return list(Paper.objects.filter(user=user, published=True))
