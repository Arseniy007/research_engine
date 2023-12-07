from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import BioForm, PageStatusForm
from .helpers import get_all_published_papers
from utils.decorators import profile_ownership_required
from utils.verification import check_profile


def profile_page_view(request, profile_id):
    # TODO

    profile = check_profile(profile_id)

    followers = profile.followers.all()
    following = len(profile.user.following.all())
    published_papers = get_all_published_papers(profile.user)

    params = {"user": profile.user, "followers": followers, "following": following, "published_papers": published_papers}

    return render(request, "profile_page/profile_page.html", params)


@login_required(redirect_field_name=None)
def follow_profile(request, profile_id):
    """Follow or unfollow user profile page"""

    profile, user = check_profile(profile_id), request.user

    # Error case (if user is trying to follow themselves)
    if profile.user == user:
        # Redirect back to profile page
        return_link = reverse("profile_page:profile_view", args=(profile_id,))
        return redirect(return_link)

    # Follow / unfollow profile user
    if user in profile.followers.all():
        profile.unfollow(user)
        status = "not followed"
    else:
        profile.follow(user)
        status = "followed"

    return JsonResponse({"status": status, "number_of_followers": len(profile.followers.all())})


@profile_ownership_required
@login_required(redirect_field_name=None)
def profile_settings(request, profile_id):
    # TODO
    # uni?
    # degree?
    # usw.?
    
    profile = check_profile(profile_id)

    pass
