import sys, traceback
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

import group_builder.apps.groups.models as group_models
import group_builder.apps.groups.forms as group_forms
import group_builder.apps.groups.lib_views as lib_views

@login_required(login_url="login/")
def home(request):
    groups = lib_views.get_all_groups(request.user)
    return render(request,"home.html", {'nodes': groups})


@login_required(login_url="login/")
def invitations(request):
    groups = lib_views.get_all_groups(request.user)
    invitations = group_models.Invitation.objects.filter(email = request.user.email)
    return render(request,"invitations.html", {'nodes': groups, 'invitations': invitations})


@login_required(login_url="login/")
def invitation_response(request, answer, group_id):
    lib_views.handle_invitation_response(request.user, answer, group_id)
    return redirect(reverse('invitations'))


@login_required(login_url="login/")
def create_group(request):
    groups = lib_views.get_all_groups(request.user)

    if(request.method == "POST"):
        group = group_models.Group.objects.create(name = request.POST.get("name", ""))
        group_models.Permission.objects.create(user = request.user, group = group, permission = group_models.Permission.SUPER_USER)
        group_models.Group.objects.create(name = "all members", parent = group)
        return redirect('home')
    else:
        form = group_forms.CreateGroupForm()
        return render(request,"create_group.html", {'nodes': groups, 'form': form})


@login_required(login_url = "login/")
def create_child(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request.user, group_id)
    if(request.method == "POST"):
        parent = group_models.Group.objects.get(id = group_id)

        if(parent.has_permission(request.user, group_models.Permission.SUPER_USER)):
            name = request.POST.get("name", "")
            group_models.Group.objects.create(name = name, parent = parent)
        return redirect('home')
    else:
        form = group_forms.CreateChildForm(id = group_id)
        return render(request,"create_group.html", {'nodes': group_tree, 'parent': group, 'form': form})



@login_required(login_url="login/")
def group(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request.user, group_id)
    return render(request,"group_base.html", {'nodes': group_tree, 'parent': parent})

@login_required(login_url="login/")
def members(request, group_id):
    group, group_tree = lib_views.get_tree_info(request.user, group_id)
    members, invites = group.get_members()
    return render(request,"members.html", {'nodes': group_tree, 'parent': group, 'members': members, 'invites': invites,})

@login_required(login_url="login/")
def add_members(request, group_id):
    group, group_tree = lib_views.get_tree_info(request.user, group_id)

    if(request.method == "POST"):
        email = request.POST.get("email", "")
        group = group_models.Group.objects.get(id = group_id)
        lib_views.handle_invite(request.user, group, email, group_models.Permission.SUPER_USER)
        return redirect(reverse('members', args = [group_id]))

    else:
        all_members = group_models.Group.objects.get(tree_id = group.tree_id, name ="all members")
        member_types = list(all_members.get_descendants(include_self=False).values('name'))
        print(member_types)
        form = group_forms.InvitationForm(member_types = member_types)
        return render(request,"add_members.html", {'nodes': group_tree, 'parent': group, 'form': form})


@login_required(login_url="login/")
def documents(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request.user, group_id)
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
    parent, group_tree = lib_views.get_tree_info(request.user, group_id)
    events = parent.get_events()
    return render(request,"timetables.html", {'parent': parent, 'nodes': group_tree, 'events': events})

@login_required(login_url="login/")
def conversations(request, group_id):
    if request.method == "POST":
        form = group_forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.sender = request.user
            post.save()
            redirect(reverse('conversations', args = [group_id]))
    else:
        parent, group_tree = lib_views.get_tree_info(request.user, group_id)
        form = group_forms.PostForm()
        return render(request,"conversations.html", {'parent': parent, 'nodes': group_tree, 'form': form})

@login_required(login_url="login/")
def create_event(request, group_id):
    parent, group_tree = lib_views.get_tree_info(request.user, group_id)

    if request.method == "POST":
        form = group_forms.EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.group = parent
            event.save()
        return redirect(reverse('timetables', args = [group_id]))

    else:
        form = group_forms.EventForm()
        return render(request,"create_event.html", {'parent': parent, 'nodes': group_tree, 'form': form})

import json
@login_required(login_url="login/")
def get_email_addresses(request, group_id):
    email_addresses = lib_views.get_members_email(request.user, group_id)
    print(email_addresses)

    if request.is_ajax():
        q = request.GET.get('term', '')

        matches = [c['email'] for c in email_addresses if q in c['email']]
        matches = set(matches)

        results = []
        for cn in matches:
            cn_json = {'value': cn}
            results.append(cn_json)
        data = json.dumps(results)
        print(data)
    else:
        print("hadddlå")
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


