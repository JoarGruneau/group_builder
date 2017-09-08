import group_builder.apps.groups.models as group_models

from django import forms
from functools import partial

DateInput = partial(forms.DateInput, {'class': 'datepicker'})
TimeInput  = partial(forms.TimeInput, {'class': 'timepicker'})

class EventForm(forms.ModelForm):

    class Meta:
        model = group_models.Event
        exclude = ('group', )
        widgets = {'start_date': DateInput() , 'start_time': TimeInput(), 'end_date': DateInput(), 'end_time': TimeInput()}

class CreateGroupForm(forms.Form):
    name = forms.CharField(label = "name", max_length = 100, required=True)

class CreateChildForm(forms.Form):
    def __init__(self, *args,**kwargs):
        parent_id = kwargs.pop('id')
        super(CreateChildForm, self).__init__(*args,**kwargs)
        self.fields['parent'] = forms.CharField(initial = parent_id, required = True)

    name = forms.CharField(label = "name", max_length = 100, required=True)

class InvitationForm(forms.ModelForm):
    class Meta:
        model = group_models.Invitation
        fields =('email', )

    # email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

class DocumentForm(forms.ModelForm):
    class Meta:
        model = group_models.Document
        fields =('docfile', )