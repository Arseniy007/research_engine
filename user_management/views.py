from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from research_engine.settings import LOGIN_URL
from utils.messages import display_error_message, display_info_message, display_success_message
from utils.verification import check_reset_password_code
from .forms import (
    AccountSettingsForm, ChangePasswordForm, ForgetPasswordForm, LoginForm, 
    ForgetPasswordForm2, RegisterForm, ResetPasswordForm, check_forget_password_form_info
)
from .helpers import get_user_by_reset_code, get_user_papers, get_user_work_spaces
from .models import User
from .password_resetting import generate_password_reset_code, get_reset_url, send_password_resetting_email


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

        # Error case
        display_error_message(request)
        return redirect(reverse("user_management:register"))

    data = {
        "page_type": "register",
        "form_title": "Register",
        "register_form": form
    }
    return render(request, "website/user_management.html", data)


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
                redirect_url = reverse("website:lobby")
                if request.POST["redirect_url"]:
                    redirect_url = request.POST["redirect_url"]
                return redirect(redirect_url)

        # Error case
        display_error_message(request, "Invalid username and/or password.")
        return redirect(LOGIN_URL)

    data = {
        "page_type": "login",
        "form_title": "Login",
        "login_form": form
    }
    return render(request, "website/user_management.html", data)


@login_required
def edit_account_info(request):
    """Update user main info"""

    if request.method == "POST":
        form = AccountSettingsForm(request.POST)

        if form.is_valid():
            user = authenticate(request, username=request.user.username, password=form.cleaned_data["password"])
            if user is not None and user == request.user:
                # Save all changes
                form.update_user_info(user)
                # Redirect to settings page
                display_success_message(request, "Account details were successfully updated!")
                return redirect(reverse("website:account_settings"))

        # Error case
        display_error_message(request)
        return redirect(reverse("user_management:edit_account"))

    data = {
        "page_type": "edit_main_info",
        "form_title": "Edit Main Info",
        "settings_form": AccountSettingsForm().set_initials(request.user),
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user)
    }
    return render(request, "website/user_management.html", data)


@login_required
def change_password(request):
    """Allow user to change their password"""

    form = ChangePasswordForm(request.POST or None)

    if request.method == "POST":
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
                return redirect(LOGIN_URL)

        # Redirect back in case of error
        display_error_message(request)
        return redirect(reverse("user_management:change_password"))

    data = {
        "page_type": "change_password",
        "form_title": "Change Password",
        "change_password_form": form,
        "work_spaces": get_user_work_spaces(request.user),
        "papers": get_user_papers(request.user)
    }
    return render(request, "website/user_management.html", data)


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

    data = {
        "page_type": "forget_password",
        "form_title": "Forget Password",
        "first_form": ForgetPasswordForm(), 
        "second_form": ForgetPasswordForm2()
    }
    return render(request, "user_management.html", data)


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

    data = {
        "page_type": "reset_password",
        "form_title": "Reset Password",
        "reset_form": form, 
        "reset_code": reset_code
    }
    return render(request, "website/user_management.html", data)


def logout_view(request):
    """Log user out"""
    logout(request)
    return redirect(LOGIN_URL)
