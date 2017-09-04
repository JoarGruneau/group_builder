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
    def __init__(self, *args,**kwargs):
        parent_id = kwargs.pop('id')
        super(MemberInvitationForm, self).__init__(*args,**kwargs)
        self.fields['parent'] = forms.CharField(initial = parent_id, required = True, widget=forms.HiddenInput())
        
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')