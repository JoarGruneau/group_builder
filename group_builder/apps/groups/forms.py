from django import forms

class CreateGroupForm(forms.Form):
    name = forms.CharField(label = "name", max_length = 100, required=True)

class CreateChildForm(forms.Form):
    def __init__(self, *args,**kwargs):
        parent_id = kwargs.pop('id')
        super(CreateChildForm, self).__init__(*args,**kwargs)
        self.fields['parent'] = forms.CharField(initial = parent_id, required = True)

    name = forms.CharField(label = "name", max_length = 100, required=True)

class MemberInvitationForm(forms.Form):        
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes')