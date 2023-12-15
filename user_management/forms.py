from django import forms
from .models import User


ATTRS = {"class": "form-control", "autocomplete": "off"}


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    first_name = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    last_name = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    email = forms.EmailField(widget=forms.TextInput(attrs=ATTRS))
    password = forms.CharField(widget=forms.PasswordInput(attrs=ATTRS))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs=ATTRS))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    password = forms.CharField(widget=forms.PasswordInput(attrs=ATTRS))


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
    username = forms.CharField(widget=forms.TextInput(attrs=ATTRS))
    

class ForgetPasswordForm2(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email",)
    


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs=ATTRS))
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs=ATTRS))

    # TODO?


class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email",)

    # TODO
    # Maybe regular form?
    