from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User
from utils.verification import check_profile_page


def profile_page_view(request, profile_id):
    # TODO

    profile = check_profile_page(profile_id)

    params = {"user": profile.user}

    return render(request, "profile_page/profile_page.html", params)


@login_required(redirect_field_name=None)
def follow_profile(request, profile_id):
    """Follow or unfollow user profile page"""

    profile, user = check_profile_page(profile_id), request.user

    # Error case (if user is trying to follow themself)
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
