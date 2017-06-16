from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import group_builder.apps.groups.models as group_models
import group_builder.apps.groups.forms as group_forms

@login_required(login_url="login/")
def create_group(request):
    if(request.method == "POST"):
        group = group_models.Group()
        group.author = request.user
        group.name = request.POST.get("name", "")
        print(group.name)
        group.publish()
        return redirect('home')

    elif(request.method == "GET"):
        form = group_forms.CreateGroupForm()
        return render(request,"create_group.html", {'form': form})