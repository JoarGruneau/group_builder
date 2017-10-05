import group_builder.apps.groups.models as group_models

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, ButtonHolder
from crispy_forms.bootstrap import FormActions, InlineCheckboxes

class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('start_date', placeholder = 'Start date', css_class="datepicker", autocomplete="off"), css_class="col-sm-2"),
                Div(Field('start_time', placeholder = 'Start time', css_class="timepicker", autocomplete="off"), css_class="col-sm-2"),
                Div(Field('end_date', placeholder = 'End date', css_class="datepicker", autocomplete="off"), css_class="col-sm-2"),
                Div(Field('end_time', placeholder = 'End time', css_class="timepicker", autocomplete="off"), css_class="col-sm-2"),
                Div(FormActions(Submit('create event', 'Create event', css_class='btn btn-success')), css_class="col-md-2"),
                css_class = 'row'),
            )
        self.helper.form_show_labels = False
    class Meta:
        model = group_models.Event
        exclude = ('group', )

class CreateGroupForm(forms.Form):
    group_rooms = forms.MultipleChoiceField(choices= group_models.Group_room.choices, widget=forms.CheckboxSelectMultiple())
    name = forms.CharField(label = "name", max_length = 100, required=True)

    def __init__(self, *args, **kwargs):
        super(CreateGroupForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('name', placeholder = 'Group name', autocomplete="off"), css_class="col-sm-5"),
                InlineCheckboxes('group_rooms'),
                Div(FormActions(Submit('create group', 'Create group', css_class='btn btn-success')), css_class="col-md-2"),
                css_class="container"
                )
            )
        self.helper.form_show_labels = False

    def process(self, request_user):
        group = group_models.Group.objects.create(name = self.cleaned_data.get('name'), group_type=group_models.Group.DEFAULT)
        group_models.Permission.objects.create(user = request_user, group = group, permission = group_models.Permission.SUPER_USER)
        group_models.Group.objects.create(name = "all members", parent = group, group_type=group_models.Group.MEMBER_GROUP)
        rooms = self.cleaned_data.get('group_rooms')
        for room in rooms:
            group_models.Group_room.objects.create(group = group, room = room)


class CreateChildForm(forms.Form):
    name = forms.CharField(label = "name", max_length = 100, required=True)
    group_rooms = forms.MultipleChoiceField(choices= group_models.Group_room.choices, widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, *args,**kwargs):
        member_choices = kwargs.pop('member_types')
        super(CreateChildForm, self).__init__(*args,**kwargs)
        self.fields['member_choice'] = forms.MultipleChoiceField(choices= member_choices, widget=forms.CheckboxSelectMultiple(), required=False)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('name', placeholder = 'Group name', autocomplete="off"), css_class="col-sm-5"),
                InlineCheckboxes('group_rooms'),
                InlineCheckboxes('member_choice'),
                Div(FormActions(Submit('create child', 'Create child', css_class='btn btn-success')), css_class="col-md-2"),
                css_class="container"
                )
            )
        self.helper.form_show_labels = False

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