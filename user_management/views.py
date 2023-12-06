from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import ChangePasswordForm
from .models import User
from utils.verification import check_user


def login_view(request):
    """Log user in"""

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return redirect(reverse("work_space:index"))
        else:
            return render(request, "user_management/login.html", {
                "message": "Invalid username and/or password."})
    else:
        return render(request, "user_management/login.html")


def logout_view(request):
    """Log user out"""

    logout(request)
    return redirect(reverse("user_management:login"))


def register(request):
    """Register new user"""
    
    if request.method == "POST":
        # Get input
        username, email = request.POST["username"], request.POST["email"]
        first_name, last_name = request.POST["first_name"], request.POST["last_name"]
        password, confirmation = request.POST["password"], request.POST["confirmation"]
        
        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "user_management/register.html", {
                "message": "Passwords must match."})
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except IntegrityError:
            return render(request, "user_management/register.html", {
                "message": "Username already taken."})
        
        login(request, user)
        return redirect(reverse("work_space:index"))
    else:
        return render(request, "user_management/register.html")


@login_required(redirect_field_name=None)
def change_password(request):
    '''Allow user to change their password'''

    form = ChangePasswordForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            # Get input
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["password"]
            confirmation = form.cleaned_data["confirmation"]

            # Check old password and confirmation
            user = authenticate(request, username=request.user.username, password=old_password)
            if user and new_password == confirmation:
                # Update password
                user.set_password(new_password)
                user.save()
                return redirect(reverse("TODO"))
            
        # Show error message if form is not valid
        print(form.errors)
        return render(request, "user_management/change_password.html", 
                        {"form": form, "error_message": "Try again!"})
    else:
        return render(request, "user_management/change_password.html", {"form": form})


def show_error_page(request):
    # TODO

    return render(request, "error_page.html")



def profile_page_view(request, user_id):
    # TODO

    user = check_user(user_id)

    pass


@login_required(redirect_field_name=None)
def follow_profile_page(request, user_id):
    """Follow or unfollow user"""

    profile_user, user = check_user(user_id), request.user

    # Error case (if user is trying to follow itself)
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
