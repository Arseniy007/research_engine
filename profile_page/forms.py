from django import forms


class BioForm(forms.Form):
    bio = forms.CharField()


class PageStatusForm(forms.Form):
    pass
