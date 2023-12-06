from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import User
from utils.verification import check_user


def profile_page_view(request, user_id):
    # TODO

    user = check_user(user_id)

    pass


@login_required(redirect_field_name=None)
def follow_profile_page(request, user_id):
    """Follow or unfollow user"""

    profile_user, user = check_user(user_id), request.user

    # Error case (if user is trying to follow themself)
    if profile_user == user:
        # Redirect back to profile page
        return_link = reverse("user_management:profile_page", args=(user_id,))
        return redirect(return_link)
    
    # Follow / unfollow profile user
    if user in profile_user.followers.all():
        profile_user.unfollow(user)
        status = "not followed"
    else:
        profile_user.follow(user)
        status = "followed"

    return JsonResponse({"status": status, "number_of_followers": len(profile_user.followers.all())})
