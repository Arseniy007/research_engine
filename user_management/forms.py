from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))


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
