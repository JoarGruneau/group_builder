import sys, traceback
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import group_builder.apps.groups.models as group_models
import group_builder.apps.groups.forms as group_forms

@login_required(login_url="login/")
def home(request):

    # if(request.method == "POST"):
    #     parent = group_models.Group.objects.get(id = request.POST.get("parent", ""))

    #     if(parent.has_permission(request.user, group_models.Permission.SUPER_USER)):
    #         name = request.POST.get("name", "")
    #         group_models.Group.objects.create(name = name, parent = parent)
    #     return redirect('home')

    # elif(request.method == "GET"):
    permissions = group_models.Permission.objects.filter(user = request.user)
    groups = []
    for permission in permissions:
        groups = groups + list(permission.group.get_descendants(include_self=True))
    return render(request,"home.html", {'nodes': groups})

@login_required(login_url="login/")
def create_group(request):
    if(request.method == "POST"):
        group = group_models.Group.objects.create(name = request.POST.get("name", ""))
        group_models.Permission.objects.create(user = request.user, group = group, permission = group_models.Permission.SUPER_USER)
        group_models.Group.objects.create(name = "all members", parent = group)
        return redirect('home')

    elif(request.method == "GET"):
        form = group_forms.CreateGroupForm()
        return render(request,"create_group.html", {'form': form})

@login_required(login_url="login/")
def group(request):
    if(request.method == "GET"):
        print("aeaa")
        try:
            id = request.GET.get("id", "")
            print("aesdsssaa")
            parent = group_models.Group.objects.get(id = id)
            if(parent.has_permission(request.user, group_models.Permission.READ)):

                groups = parent.get_descendants(include_self=True)
                print(groups)
                print(parent)
                breadcrums = []
                print("aesdsssaammmm")
                return render(request,"group_base.html", {'nodes': groups, 'parent': parent})
        except Exception:
            print ("Exception in user code:")
            traceback.print_exc(file=sys.stdout)
            print("weere")
            return redirect('home')

@login_required(login_url="login/")
def members(request):
    if(request.method == "GET"):
        id = request.GET.get("id", "")
        parent = group_models.Group.objects.get(id = id)
        if(parent.has_permission(request.user, group_models.Permission.READ)):
            groups = parent.get_descendants(include_self=True)
            members = parent.get_members()
            print("this is the members")
            print(members)
            return render(request,"members.html", {'nodes': groups, 'parent': parent, 'members': members})
        # except Exception:
        #     return redirect('home')

@login_required(login_url="login/")
def documents(request):
    return render(request,"documents.html")

@login_required(login_url="login/")
def conversations(request):
    return render(request,"conversations.html")