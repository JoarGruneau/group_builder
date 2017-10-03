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
    def __init__(self, *args,**kwargs):
        member_choices = kwargs.pop('member_types')
        super(CreateChildForm, self).__init__(*args,**kwargs)
        self.fields['member_choice'] = forms.MultipleChoiceField(choices= member_choices, widget=forms.CheckboxSelectMultiple(), required=False)
    name = forms.CharField(label = "name", max_length = 100, required=True)
    group_rooms = forms.MultipleChoiceField(choices= group_models.Group_room.choices, widget=forms.CheckboxSelectMultiple(), required=False)

    def process(self, parent):
        is_member_group = group_models.Group.objects.filter(
            tree_id=parent.tree_id, lft__lte = parent.lft, rght__gte = parent.rght, group_type = group_models.Group.MEMBER_GROUP).exists()

        if is_member_group:
            group_models.Group.objects.create(name = self.cleaned_data.get('name'), parent = parent, group_type=group_models.Group.MEMBER_SUB)
        else:
            group_models.Group.objects.create(name = self.cleaned_data.get('name'), parent = parent, group_type=group_models.Group.DEFAULT)

        rooms = self.cleaned_data.get('group_rooms')
        for room in rooms:
            group_models.Group_room.objects.create(group = parent, room = room)

class InvitationForm(forms.ModelForm):
    def __init__(self, *args,**kwargs):
        member_types = kwargs.pop('member_types')
        super(InvitationForm, self).__init__(*args,**kwargs)
        member_choices = group_models.Permission.permission_choice
        self.offset = len(group_models.Permission.permission_choice)

        for member_type in member_types:
            member_choices += ((member_type[0] + self.offset, member_type[1]),)

        self.fields['member_choice'] = forms.ChoiceField(choices= member_choices)

        def process(self, request_user, parent):
            member_type = self.cleaned_data.get('member_choice')
            if member_type <= self.offset:
                group_models.Default_invitation.create(email = self.cleaned_data.get('email'), 
                    group = parent, invited_by = request_user, member_type = member_type)
            else:
                group_models.Custom_invitation.create(email = self.cleaned_data.get('email'), 
                    group = parent, invited_by = request_user, member_type = group_models.Group.objects.get(id = member_type - self.offset))

    class Meta:
        model = group_models.Default_invitation
        fields =('email',)
        widgets = {'email': forms.TextInput(attrs={'id': 'autocomplete-email'}),}

    def process(self):
        group_models.Invitation.objects.create()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = group_models.Document
        fields =('docfile', )

class PostForm(forms.ModelForm):
    class Meta:
        model = group_models.Post
        fields = ('message',)