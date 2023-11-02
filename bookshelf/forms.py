from django import forms

from .models import Book, Quote


class NewBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        exclude = ["user"]
    
    # add exsta fields here

    """
    widgets = {
    
            "name": Textarea(attrs={"cols": 80, "rows": 20}),
    }
    """
    pass


class AlterBookForm(forms.ModelForm):
    class Meta:
        model = Book
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
        model = Quote
        fields = "__all__"
        exclude = []
    
     # add exsta fields here