from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import ChangePasswordForm, LoginForm
from .models import User
from utils.messages import display_error_message


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
        
        #login(request, user) # TODO
        return redirect(reverse("user_management:login"))
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
