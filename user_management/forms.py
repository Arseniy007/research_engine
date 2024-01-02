from django import forms
from .models import User
from .user_finder import get_user_by_name, get_user_by_username


ATTRS = {"class": "form-control", "autocomplete": "off"}

_CLASS = "form-control form-control-lg"


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": _CLASS,
        "autocomplete": "off"})                 
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "first-name-field",
        "class": _CLASS})
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "last-name-field",
        "class": _CLASS})
    )

    email = forms.EmailField(widget=forms.TextInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": _CLASS})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": _CLASS})
    )

    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": _CLASS})
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": _CLASS,
        "autocomplete": "off"})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": _CLASS})
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "placeholder": "Old password",
        "autocomplete": "off",
        "id": "old_password"})
    )

    password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "placeholder": "New password",
        "autocomplete": "off",
        "id": "new_password"})
    )

    confirmation = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "placeholder": "Confirm new password",
        "autocomplete": "off",
        "id": "confirmation"})
    )


class ForgetPasswordForm(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "first_form"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": _CLASS,
        "autocomplete": "off"})
    )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": _CLASS})
    )


class ForgetPasswordForm2(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "second_form"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "first-name-field",
        "class": _CLASS})
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "last-name-field",
        "class": _CLASS})
    )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": _CLASS})
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": _CLASS})
    )

    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": _CLASS})
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




class AccountDetailsForm(forms.Form):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs=ATTRS))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs=ATTRS))
    date_of_birth = forms.CharField(required=False, widget=forms.DateInput(attrs=ATTRS))


class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

    # TODO
    # Maybe regular form?
