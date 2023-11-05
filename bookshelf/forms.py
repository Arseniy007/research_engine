from django import forms

from research_engine.settings import ACCEPTED_UPLOAD_FORMATS
from .models import Book


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "author", "multiple_authors", "file"]


    author_last_name = forms.CharField(max_length=40)
    author_first_name = forms.CharField(max_length=40)
    author_second_name = forms.CharField(max_length=40)


class UploadBookForm(forms.Form):

    file = forms.FileField(widget=forms.FileInput(attrs={"accept": ACCEPTED_UPLOAD_FORMATS}))


class AlterBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "multiple_authors"]
    
    # add exsta fields here

    """
    widgets = {
            "name": Textarea(attrs={"cols": 80, "rows": 20}),
    }
    """
    pass


"""
class NewQuoteForm(forms.ModelForm):
    class Meta:
        model = ""
        fields = "__all__"
        exclude = []
    
     # add exsta fields here
"""