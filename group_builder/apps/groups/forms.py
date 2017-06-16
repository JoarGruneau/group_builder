from django import forms

class CreateGroupForm(forms.Form):
    group_name = forms.CharField(label = "group name", max_length = 100, required=True)