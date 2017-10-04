from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Div, ButtonHolder
from crispy_forms.bootstrap import FormActions, InlineField

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('username', placeholder = 'Email'), css_class="col-sm-5"),
                Div(Field('password', placeholder = 'Password'), css_class="col-sm-5"),
                ButtonHolder(Submit('login', 'Login', css_class='btn btn-success btn-sm')),
                css_class = 'row'),
            )
        self.helper.form_show_labels = False


    # username = forms.CharField(label="Username", max_length=30, 
    #                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    # password = forms.CharField(label="Password", max_length=30, 
    #                            widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Div(Field('first_name', placeholder = 'First name'), css_class="col-sm-5"),
                Div(Field('last_name', placeholder = 'Last name'), css_class="col-sm-5"),
                css_class = 'row'
            ),
            Div(Div(Field('email', placeholder = 'Email'), css_class="col-sm-5"), css_class = 'row'),
            Div(
                Div(Field('password1', placeholder = 'Password'), css_class="col-sm-5"),
                Div(Field('password2', placeholder = 'Password confirmation'), css_class="col-sm-5"),
                css_class='row'
            ),
            ButtonHolder(Submit('register', 'Register', css_class='btn btn-success btn-sm'))
            )
        self.helper.form_show_labels = False


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )

    def save(self):
        user = super(RegisterForm, self).save(commit = False)
        user.username = self.cleaned_data.get('email')
        user.save()
