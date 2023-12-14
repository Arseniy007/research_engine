from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import ChangePasswordForm, LoginForm, RegisterForm, ResetPasswordForm
from .models import User
from .password_resetting import generate_password_reset_code, get_reset_url, send_password_resetting_email
from research_engine.settings import LOGIN_URL
from utils.messages import display_error_message, display_success_message
from utils.verification import check_reset_password_code


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
    """Send user an email with password-reset url"""
    # TODO

    # Get unique reset code and create reset url 
    reset_code = generate_password_reset_code(request.user)
    reset_url = get_reset_url(request, reset_code)

    # Send user "I-forgot-password" email
    send_password_resetting_email(request.user, reset_url)

    # TODO where to redirect?
    return redirect(reverse("website:index"))


@login_required(redirect_field_name=None)
def reset_forgotten_password(request, reset_code):
    """Reset user password ;)"""

    form = ResetPasswordForm(request.POST or None)

    if request.method == "POST":
        if form and form.is_valid():
            reset_code = check_reset_password_code(reset_code, request.user)
            
            if not reset_code:
                # Error case (wrong reset code)
                display_error_message(request)
                return redirect(LOGIN_URL)
        
            # TODO Delete reset code, set new password etc.
         
            display_success_message(request, "Password was successfully updated!")
            return redirect(LOGIN_URL)
        
        # Error case
        display_error_message(request)
        return redirect(reverse("user_management:reset_password", args=(reset_code,)))
    return render(request, "user_management/reset_password.html", {"form": form})


def logout_view(request):
    """Log user out"""
    logout(request)
    return redirect(LOGIN_URL)
