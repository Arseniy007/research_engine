from django import forms

from .models import Book


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user", "work_space", "author", "is_edited"]


    author_last_name = forms.CharField(max_length=40)
    author_first_name = forms.CharField(max_length=40) 
    
    # add exsta fields here

    """
    widgets = {
    
            "name": Textarea(attrs={"cols": 80, "rows": 20}),
    }
    """
    pass


class AlterBookForm(forms.ModelForm):
    class Meta:
        model = ""
        fields = "__all__"
        exclude = ["user"]
    
    # add exsta fields here

    """
    widgets = {
    
            "name": Textarea(attrs={"cols": 80, "rows": 20}),
    }
    """
    pass


class NewQuoteForm(forms.ModelForm):
    class Meta:
        model = ""
        fields = "__all__"
        exclude = []
    
     # add exsta fields here