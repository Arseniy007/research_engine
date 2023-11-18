from django import forms



class TestForm(forms.Form):


    field_1 = forms.CharField(widget=forms.TextInput(attrs={"class": "one"}))
    field_2 = forms.CharField(widget=forms.TextInput(attrs={"class": "two"}))
    field_3 = forms.CharField(widget=forms.TextInput(attrs={"class": "three"}))
    field_4 = forms.CharField(widget=forms.TextInput(attrs={"class": "four"}))
    field_5 = forms.CharField(widget=forms.TextInput(attrs={"class": "five"}))