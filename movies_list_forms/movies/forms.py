from django import forms

class MovieForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=3, required=True)
    actors = forms.CharField(widget=forms.Textarea, max_length=1000, min_length=3, required=True)
    year = forms.IntegerField(min_value=1888, max_value=2025)