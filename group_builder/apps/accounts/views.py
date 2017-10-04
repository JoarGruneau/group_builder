from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import group_builder.apps.accounts.forms as accounts_forms

def register(request):
    if(request.method == 'POST'):
        form = accounts_forms.RegisterForm(request.POST)
        if(form.is_valid()):
            form.save()
            username = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = accounts_forms.RegisterForm()
    return render(request, "register.html", {'form': form})
