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
    group_rooms = forms.MultipleChoiceField(choices= group_models.Group_room.choices, widget=forms.CheckboxSelectMultiple())
    name = forms.CharField(label = "name", max_length = 100, required=True)

    def process(self, request_user):
        group = group_models.Group.objects.create(name = self.cleaned_data.get('name'), group_type=group_models.Group.DEFAULT)
        group_models.Permission.objects.create(user = request_user, group = group, permission = group_models.Permission.SUPER_USER)
        group_models.Group.objects.create(name = "all members", parent = group, group_type=group_models.Group.MEMBER_GROUP)
        rooms = self.cleaned_data.get('group_rooms')
        for room in rooms:
            group_models.Group_room.objects.create(group = group, room = room)

class CreateChildForm(forms.Form):
    group_rooms = forms.MultipleChoiceField(choices= group_models.Group_room.choices, widget=forms.CheckboxSelectMultiple())
    name = forms.CharField(label = "name", max_length = 100, required=True)

    def process(self, parent):
        group_models.Group.objects.create(name = self.cleaned_data.get('name'), parent = parent)
        rooms = self.cleaned_data.get('group_rooms')
        for room in rooms:
            group_models.Group_room.objects.create(group = parent, room = room)

class InvitationForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        member_types = kwargs.pop('member_types')
        super(InvitationForm, self).__init__(*args,**kwargs)
        member_choices = group_models.Permission.permission_choice
        for element in member_types:
            member_type = element['name']
            member_choices += ((member_type, member_type), )

        self.fields['member_choices'] = forms.ChoiceField(choices= member_choices)

    class Meta:
        model = group_models.Invitation
        fields =('email', )
        widgets = {'email': forms.TextInput(attrs={'id': 'autocomplete-email'})}

class DocumentForm(forms.ModelForm):
    class Meta:
        model = group_models.Document
        fields =('docfile', )

class PostForm(forms.ModelForm):
    class Meta:
        model = group_models.Post
        fields = ('message',)