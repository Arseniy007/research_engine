from django import forms
from research_engine.constants import CLASS_
from .helpers import get_user_by_name, get_user_by_username
from .models import User


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Username"})                 
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "last-name-field",
        "class": CLASS_,
        "placeholder": "Last name"})
    )

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "first-name-field",
        "class": CLASS_,
        "placeholder": "First name"})
    )

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": CLASS_,
        "placeholder": "Email"})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": CLASS_,
        "placeholder": "Password"})
    )

    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": CLASS_,
        "placeholder": "Repeat Password"})
    )


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Username"})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": CLASS_,
        "placeholder": "Password"})
    )


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "old_password-field",
        "class": CLASS_,
        "placeholder": "Old Password"})
    )

    new_password = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "new_password-field",
        "class": CLASS_,
        "placeholder": "New Password"})
    )

    confirmation = forms.CharField(label=False, widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": CLASS_,
        "placeholder": "Repeat New Password"})
    )


class ForgetPasswordForm(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "first_form"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "username-field",
        "class": CLASS_,
        "autocomplete": "off",
        "placeholder": "Username"})
    )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": CLASS_,
        "placeholder": "Email"})
    )


class ForgetPasswordForm2(forms.Form):
    form_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": "second_form"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "first-name-field",
        "class": CLASS_,
        "placeholder": "First name"})
    )

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text",
        "id": "last-name-field",
        "class": CLASS_,
        "placeholder": "Last name"})
    )

    email = forms.CharField(widget=forms.EmailInput(attrs={
        "type": "email",
        "id": "email-field",
        "class": CLASS_,
        "placeholder": "Email"})
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "password-field",
        "class": CLASS_,
        "placeholder": "New Password"})
    )

    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password",
        "id": "confirmation-field",
        "class": CLASS_,
        "placeholder": "Repeat Password"})
    )


class AccountSettingsForm(RegisterForm):
    confirmation = forms.CharField(required=False)

    def set_initials(self, user: User):
        """Pre-populate fields"""
        self.fields["username"].initial = user.username
        self.fields["last_name"].initial = user.last_name
        self.fields["first_name"].initial = user.first_name
        self.fields["email"].initial = user.email
        return self

    
    def update_user_info(self, user: User):
        """Save all changes"""
        user.username = self.cleaned_data["username"]
        user.last_name = self.cleaned_data["last_name"]
        user.first_name = self.cleaned_data["first_name"]
        user.email = self.cleaned_data["email"]
        user.save(update_fields=("username", "last_name", "first_name", "email",))


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
