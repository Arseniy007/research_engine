from django import forms


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
