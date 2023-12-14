from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import ChangePasswordForm, LoginForm, RegisterForm
from .models import User
from research_engine.settings import LOGIN_URL
from utils.messages import display_error_message


def register(request):
    """Register new user"""

    form = RegisterForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            # Get input
            form.cleaned_data[""]
            username, email = form.cleaned_data["username"], form.cleaned_data["email"]
            first_name, last_name = form.cleaned_data["first_name"], form.cleaned_data["last_name"]
            password, confirmation = form.cleaned_data["password"], form.cleaned_data["confirmation"]
            
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
            
            return redirect(LOGIN_URL)
        else:
            display_error_message(request)
    return render(request, "user_management/register.html", {"register_form": form})


def login_view(request):
    """Log user in"""

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            # Attempt to sign user in
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)

                # Get proper redirect url (index by default)
                redirect_url = reverse("website:index")
                if request.POST["redirect_url"]:
                    redirect_url = request.POST["redirect_url"]
                return redirect(redirect_url)
            else:
                return render(request, "user_management/login.html", {
                    "message": "Invalid username and/or password."})
        else:
            display_error_message(request)
    return render(request, "user_management/login.html", {"login_form": form})


@login_required(redirect_field_name=None)
def change_password(request):
    """Allow user to change their password"""

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
            
        # Redirect back in case of error
        display_error_message(request)
        return redirect(reverse("user_management:change_password"))
    
    return render(request, "user_management/change_password.html", {"form": form})


@login_required(redirect_field_name=None)
def forget_password(request):
    """TODO"""

    pass


def logout_view(request):
    """Log user out"""
    logout(request)
    return redirect(LOGIN_URL)
