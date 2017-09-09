import sys, traceback
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import group_builder.apps.groups.models as group_models
import group_builder.apps.groups.forms as group_forms
import group_builder.apps.groups.lib_views as lib_views

@login_required(login_url="login/")
def home(request):
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

@login_required(login_url = "login/")
def create_child(request, group_id):
    if(request.method == "POST"):
        parent = group_models.Group.objects.get(id = group_id)

        if(parent.has_permission(request.user, group_models.Permission.SUPER_USER)):
            name = request.POST.get("name", "")
            group_models.Group.objects.create(name = name, parent = parent)
        return redirect('home')
    elif(request.method == "GET"):
        form = group_forms.CreateChildForm(id = group_id)
        return render(request,"create_group.html", {'form': form})



@login_required(login_url="login/")
def group(request, group_id):
    if(request.method == "GET"):
        try:
            parent, group_tree = lib_views.get_tree_info(request, group_id)
            return render(request,"group_base.html", {'nodes': group_tree, 'parent': parent})
        except Exception:
            print ("Exception in user code:")
            traceback.print_exc(file=sys.stdout)
            print("weere")
            return redirect('home')

@login_required(login_url="login/")
def members(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request, group_id)

    if(request.method == "POST"):
        form = group_forms.InvitationForm(request.POST)

        email = request.POST.get("email", "")
        parent = group_models.Group.objects.get(id = group_id)

        if parent.has_permission(request.user, group_models.Permission.SUPER_USER):
            if(parent.member_exsist(email)):
                group_models.Permission.objects.create(user = request.user, group = parent, permission = group_models.Permission.SUPER_USER)
            else:
                if not parent.has_invitation(email = email, permission_type = group_models.Permission.SUPER_USER):
                    group_models.Invitation.objects.create(email = email, group =parent, 
                        invited_by = request.user, permission = group_models.Permission.SUPER_USER)
        return redirect(reverse('members', args = [group_id]))

    else:
        members, invites = parent.get_members()
        form = group_forms.InvitationForm()
        return render(request,"members.html", {'nodes': group_tree, 'parent': parent, 'members': members, 'invites': invites, 'form': form})



@login_required(login_url="login/")
def documents(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request, group_id)
    if request.method == 'POST':
        form = group_forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = group_models.Document(docfile = request.FILES['docfile'], group = parent)
            newdoc.save()
            return redirect(reverse('documents', args = [group_id]))
    else:
        form = group_forms.DocumentForm()

    documents = parent.get_documents()
    print(documents)
    return render(request,"documents.html", {'parent': parent, 'nodes': group_tree, 'documents': documents, 'form': form})

@login_required(login_url = "login/")
def timetables(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request, group_id)
    events = parent.get_events()
    return render(request,"timetables.html", {'parent': parent, 'nodes': group_tree, 'events': events})

@login_required(login_url="login/")
def conversations(request, group_id):
    return render(request,"conversations.html")

@login_required(login_url="login/")
def create_event(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request, group_id)

    if request.method == "POST":
        form = group_forms.EventForm(request.POST)
        form.group = parent
        if form.is_valid():
            event = form.save(commit=False)
            event.group = parent
            event.save()
        return redirect(reverse('timetables', args = [group_id]))

    else:
        form = group_forms.EventForm()
        return render(request,"create_event.html", {'parent': parent, 'nodes': group_tree, 'form': form})


