from django import forms



class NewWorkSpaceForm(forms.Form):

    title = forms.CharField(max_length=50)



class RenameWorkSpaceForm(forms.Form):

    new_title = forms.CharField(max_length=50)
