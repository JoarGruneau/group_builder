from django import forms

class CreateGroupForm(forms.Form):
    name = forms.CharField(label = "name", max_length = 100, required=True)

class CreateChildForm(forms.Form):
    def __init__(self, *args,**kwargs):
        parent_id = kwargs.pop('id')
        super(CreateChildForm, self).__init__(*args,**kwargs)
        self.fields['parent'] = forms.CharField(initial = parent_id, required = True)

    name = forms.CharField(label = "name", max_length = 100, required=True)