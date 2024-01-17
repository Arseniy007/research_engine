from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import *
from .helpers import get_user_by_reset_code, get_users_work_spaces
from .models import User
from .password_resetting import generate_password_reset_code, get_reset_url, send_password_resetting_email
from research_engine.settings import LOGIN_URL
from utils.decorators import post_request_required
from utils.messages import display_error_message, display_info_message, display_success_message
from utils.verification import check_reset_password_code


def register(request):
    """Register new user"""

    form = RegisterForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            # Get input
            username, email = form.cleaned_data["username"], form.cleaned_data["email"]
            first_name, last_name = form.cleaned_data["first_name"], form.cleaned_data["last_name"]
            password, confirmation = form.cleaned_data["password"], form.cleaned_data["confirmation"]
            
            # Ensure password matches confirmation
            if password != confirmation:
                display_error_message(request, "Passwords must match")
                return redirect("user_management:register")
            
            # Attempt to create new user
            try:
                user = User.objects.create_user(username, email, password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
            except IntegrityError:
                display_error_message(request, "Username already taken")
                return redirect("user_management:register")
            
            return redirect(LOGIN_URL)
        else:
            display_error_message(request)
            return redirect(reverse("user_management:register"))
    return render(request, "user_management/register.html", {"register_form": form})


def login_view(request):
    """Log user in"""

    # Log out user first
    logout(request)

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
            
        # Error case
        display_error_message(request, "Invalid username and/or password.")
        return redirect(LOGIN_URL)

    return render(request, "user_management/login.html", {"login_form": form})


@login_required(redirect_field_name=None)
def account_settings(request):
    """Update user info"""

    if request.method == "POST": 
        settings_form = AccountSettingsForm(request.POST)

        if settings_form.is_valid():
            user = authenticate(request, username=request.user.username, password=settings_form.cleaned_data["password"])
            if user is not None and user == request.user:
                # Save all changes
                settings_form.update_user_info(user)
                # Redirect to login-view
                display_success_message(request, "Account details were successfully updated!")
                return JsonResponse({"status": "ok"})

        # Error case
        display_error_message(request)
        return JsonResponse({"status": "error"})

    data = {
        "change_password_form": ChangePasswordForm(),
        "settings_form": AccountSettingsForm().set_initials(request.user),
        "work_spaces": get_users_work_spaces(request.user)
    }
    return render(request, "user_management/account_settings.html", data)


@login_required
@post_request_required
def change_password(request):
    """Allow user to change their password"""

    form = ChangePasswordForm(request.POST)

    if form.is_valid():
        old_password = form.cleaned_data["old_password"]
        new_password = form.cleaned_data["new_password"]
        confirmation = form.cleaned_data["confirmation"]

        # Check old password and confirmation
        user = authenticate(request, username=request.user.username, password=old_password)
        if user and new_password == confirmation:
            # Update password
            user.set_password(new_password)
            user.save(update_fields=("password",))
            display_success_message(request, "Password was successfully updated!")
            return JsonResponse({"status": "ok"})
        
    # Redirect back in case of error
    display_error_message(request)
    return JsonResponse({"status": "error"})
    

def forget_password(request):
    """Send user an email with password-reset url"""

    if request.method == "POST":
        # Check if user submitted right info
        user = check_forget_password_form_info(request)
        if user:
            # Get unique reset code and create resets url 
            reset_code = generate_password_reset_code(user)
            reset_url = get_reset_url(request, reset_code)

            # Send user "I-forgot-password" email
            send_password_resetting_email(user, reset_url)

            # Redirect back to login view
            display_info_message(request, "Check your email")
            return redirect(LOGIN_URL)
        
        # Error case
        display_error_message(request)
        return redirect(reverse("user_management:forget_password"))
        
    forms = {
        "first_form": ForgetPasswordForm(), 
        "second_form": ForgetPasswordForm2()
    }
    return render(request, "user_management/forget_password.html", forms)


def reset_password(request, reset_code):
    """Reset user forgotten password ;)"""

    # Check reset_code
    user = get_user_by_reset_code(reset_code)
    reset_code_obj = check_reset_password_code(reset_code, user)
    if not reset_code_obj:
        # Error case (wrong reset code)
        display_error_message(request, "This url is no longer valid")
        return redirect(LOGIN_URL)

    form = ResetPasswordForm(request.POST or None)
    if request.method == "POST":
        if form and form.is_valid():
            # Get form input
            new_password = form.cleaned_data["new_password"]
            confirmation = form.cleaned_data["confirmation"]

            # Check new password
            if new_password == confirmation:
                # Delete reset code from the db
                reset_code_obj.delete()

                # Update user password
                user.set_password(new_password)
                user.save(update_fields=("password",))

                # Finally redirect to login view
                display_success_message(request, "Password was successfully updated!")
                return redirect(LOGIN_URL)

        # Error case (form is not valid)
        display_error_message(request, "Passwords don't match")
        return redirect(reverse("user_management:reset_password", args=(reset_code,)))
    
    return render(request, "user_management/reset_password.html", {"reset_form": form, "reset_code": reset_code})


def logout_view(request):
    """Log user out"""
    logout(request)
    return redirect(LOGIN_URL)
