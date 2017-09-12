import group_builder.apps.groups.models as group_models
from django.core.exceptions import PermissionDenied

def get_all_groups(request):
    permissions = group_models.Permission.objects.filter(user = request.user)
    groups = []
    for permission in permissions:
        groups = groups + list(permission.group.get_descendants(include_self=True))
    return groups

def get_group(group_id):
    return group_models.Group.objects.get(id = group_id)

def get_tree_info(request, group_id):
    group = get_group(group_id)
    if group.has_permission(request.user, group_models.Permission.READ):
        tree = group.get_descendants(include_self=True)
        return group, tree
    else:
        raise PermissionDenied()

def add_parent_and_save(form, parent):
    if form.is_valid():
        model = form.save(commit=False)
        model.parent = parent
        model.save()

def handle_invitation_response(user, answer, group_id):
    group = get_group(group_id)
    invitations = list(group_models.Invitation.objects.filter(email = user.email, group = group))
    if(len(invitations) == 1):
        invitation = invitations[0]
        if answer == "1":
            group_models.Permission.objects.create(user = user, group = group, permission = invitation.permission)

        print(invitation.id)
        print(group_models.Permission.objects.filter(id = invitation.id))
        group_models.Invitation.objects.filter(id = invitation.id).delete()

    else:
        PermissionDenied("Expected 1 invitation but " + str(len(invitations)) +" invitations found")