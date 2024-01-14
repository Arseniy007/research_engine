from django import forms
from .models import User
from .user_finder import get_user_by_name, get_user_by_username


ATTRS = {"class": "form-control", "autocomplete": "off"}

_CLASS = "form-control"


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Username"})                 
    )
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "first-name-field",
        "class": _CLASS,
        "placeholder": "First name"})
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "last-name-field",
        "class": _CLASS,
        "placeholder": "Last name"})
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": _CLASS,
        "placeholder": "Email"})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": _CLASS,
        "placeholder": "Password"})
    )

    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": _CLASS,
        "placeholder": "Repeat Password"})
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Username"})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": _CLASS,
        "placeholder": "Password"})
    )


class AccountSettingsForm(RegisterForm):
    pass


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "old_password-field",
        "class": _CLASS,
        "placeholder": "Old Password"})
    )

    new_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "new_password-field",
        "class": _CLASS,
        "placeholder": "New Password"})
    )

    confirmation = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": _CLASS,
        "placeholder": "Repeat New Password"})
    )


class ForgetPasswordForm(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "first_form"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": _CLASS,
        "autocomplete": "off",
        "placeholder": "Username"})
    )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": _CLASS,
        "placeholder": "Email"})
    )


class ForgetPasswordForm2(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "second_form"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "first-name-field",
        "class": _CLASS,
        "placeholder": "First name"})
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "last-name-field",
        "class": _CLASS,
        "placeholder": "Last name"})
    )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": _CLASS,
        "placeholder": "Email"})
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": _CLASS,
        "placeholder": "New Password"})
    )

    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": _CLASS,
        "placeholder": "Repeat Password"})
    )


def check_forget_password_form_info(request) -> User | None:
    """Get form type and check submitted data"""

    if "first_form" in request.POST["form_type"]:
        form = ForgetPasswordForm(request.POST)
        if form.is_valid():
            return get_user_by_username(form.cleaned_data["username"], form.cleaned_data["email"])
    if "second_form" in request.POST["form_type"]:
        form = ForgetPasswordForm2(request.POST)
        if form.is_valid():
            return get_user_by_name(form.cleaned_data["first_name"], form.cleaned_data["last_name"], form.cleaned_data["email"])
    return None
