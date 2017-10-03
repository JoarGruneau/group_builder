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
        form = group_forms.CreateGroupForm(request.POST)
        if form.is_valid():
            print("hej")
            form.process(request.user)
        return redirect('home')
    else:
        form = group_forms.CreateGroupForm()
        return render(request,"create_group.html", {'nodes': groups, 'form': form})


@login_required(login_url = "login/")
def create_child(request, group_id):
    group_info = lib_views.get_group_base_info(request.user, group_id)
    member_types = lib_views.get_member_types(group_info['parent'])
    if(request.method == "POST"):
        form = group_forms.CreateChildForm(request.POST, member_types = member_types)
        if form.is_valid():
            if(group_info['parent'].has_permission(request.user, group_models.Permission.SUPER_USER)):
                form.process(group_info['parent'])
        return redirect('home')
    else:
        group_info['form'] = group_forms.CreateChildForm(member_types = member_types)
        return render(request,"create_group.html", group_info)



@login_required(login_url="login/")
def group(request, group_id):
    group_info = lib_views.get_group_base_info(request.user, group_id)
    return render(request,"group_base.html", group_info)

@login_required(login_url="login/")
def members(request, group_id):
    group_info = lib_views.get_group_base_info(request.user, group_id)
    members, invites = group_info['parent'].get_members()
    group_info['members'] = members
    group_info['invites'] = invites
    return render(request,"members.html", group_info)

@login_required(login_url="login/")
def add_members(request, group_id):
    group_info = lib_views.get_group_base_info(request.user, group_id)
    member_types = lib_views.get_member_types(group_info['parent'])
    if(request.method == "POST"):
        form = group_forms.InvitationForm(request.POST, member_types = member_types)
        if form.is_valid():
            form.process(request.user, group_info['parent'], )
        return redirect(reverse('members', args = [group_id]))

    else:
        group_info['form'] = group_forms.InvitationForm(member_types = member_types)
        return render(request,"add_members.html", group_info)


@login_required(login_url="login/")
def documents(request, group_id):
    group_info = lib_views.get_group_base_info(request.user, group_id)
    if request.method == 'POST':
        form = group_forms.DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = group_models.Document(docfile = request.FILES['docfile'], group = parent)
            newdoc.save()
            return redirect(reverse('documents', args = [group_id]))
    else:
        form = group_forms.DocumentForm()

    group_info['documents'] = group_info['parent'].get_documents()
    return render(request,"documents.html", group_info)

@login_required(login_url = "login/")
def timetables(request, group_id):
    group_info = lib_views.get_group_base_info(request.user, group_id)
    group_info['events'] = group_info['parent'].get_events()
    return render(request,"timetables.html", group_info)

@login_required(login_url="login/")
def posts(request, group_id):
    if request.method == "POST":
        form = group_forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.sender = request.user
            post.save()
            redirect(reverse('posts', args = [group_id]))
    else:
        group_info = lib_views.get_group_base_info(request.user, group_id)
        group_info['form'] = group_forms.PostForm()
        return render(request,"conversations.html", group_info)

@login_required(login_url="login/")
def create_event(request, group_id):
    group_info = lib_views.get_tree_info(request.user, group_id)

    if request.method == "POST":
        form = group_forms.EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.group = parent
            event.save()
        return redirect(reverse('timetables', args = [group_id]))

    else:
        group_info['form'] = group_forms.EventForm()
        return render(request,"create_event.html", group_info)

import json
@login_required(login_url="login/")
def get_email_addresses(request, group_id):
    email_addresses = lib_views.get_members_email(request.user, group_id)
    print(email_addresses)

    if request.is_ajax():
        q = request.GET.get('term', '')

        matches = [c['user__email'] for c in email_addresses if q in c['user__email']]
        matches = set(matches)

        results = []
        for cn in matches:
            cn_json = {'value': cn}
            results.append(cn_json)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


