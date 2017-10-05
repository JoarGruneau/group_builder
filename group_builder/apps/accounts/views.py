from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views, login, authenticate
import group_builder.apps.accounts.forms as accounts_forms

def login_register(request):
    if(request.method == 'POST'):
        if 'login' in request.POST:
            views.login(request)
        else:
            register_form = accounts_forms.RegisterForm(request.POST)
            if(register_form.is_valid()):
                register_form.save()
                username = register_form.cleaned_data.get('email')
                raw_password = register_form.cleaned_data.get('password1')
                user = authenticate(username = username, password = raw_password)
                login(request, user)
        return redirect('home')

    else:
        login_form = accounts_forms.LoginForm()
        register_form = accounts_forms.RegisterForm()
        return render(request, "base_log_in.html", {'login_form': login_form, 'register_form': register_form})
