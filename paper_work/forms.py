from django import forms


class NewPaperForm(forms.Form):
    
    title = forms.CharField(max_length=50)


class RenamePaperForm(forms.Form):

    new_title = forms.CharField(max_length=50)

