from django import forms

class CreateGroupForm(forms.Form):
    name = forms.CharField(label = "name", max_length = 100, required=True)