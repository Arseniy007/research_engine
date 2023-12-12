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


def get_all_published_papers(user: User) -> dict:
    """Get all papers (and its latest files) marked as published for given user"""
    papers = list(Paper.objects.filter(user=user, archived=False, published=True))
    return {paper.title: paper.get_last_file_id() for paper in papers}


def get_profile_status(user: User, profile: ProfilePage) -> str:
    """Check if user if owner, follower or neither"""
    user_profile_id = get_profile_id(user)
    if user_profile_id == profile.pk:
        return "owner"
    if user in profile.followers.all():
        return "follower"
    return "none"
