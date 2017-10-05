import group_builder.apps.groups.models as group_models
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

def get_group(request_user, group_id):
    group = group_models.Group.objects.get(id = group_id)
    if group.has_permission(request_user, group_models.Permission.READ):
        return group
    else:
        PermissionDenied("User: " + request_user.email + " does not have permission to view this group")

def get_tree_info(request_user, group_id):
    group = get_group(request_user, group_id)
    if group.has_permission(request_user, group_models.Permission.READ):
        tree = group.get_descendants(include_self=True)
        return group, tree
    else:
        raise PermissionDenied()

def get_all_groups(request_user):
    permissions = group_models.Permission.objects.filter(user = request_user)
    groups = []
    for permission in permissions:
        groups = groups + list(permission.group.get_descendants(include_self=True))
    return groups
    group = group_models.Group.objects.get(id = group_id)

def get_group_base_info(request_user, group_id):
    group, tree = get_tree_info(request_user, group_id)
    is_super_user = group_models.Permission.objects.filter(user = request_user, permission = group_models.Permission.SUPER_USER,
        group__tree_id=group.tree_id, group__lft__lte = group.lft, group__rght__gte = group.rght).exists()
    return {'super_user': is_super_user, 'parent': group, 'nodes': tree, 'rooms': group.get_rooms()}

def get_member_types(group):
    member_groups = group_models.Group.objects.filter(tree_id = group.tree_id, group_type = group_models.Group.MEMBER_SUB)
    result = []
    for member_group in member_groups:
        result += [[member_group.id, member_group.name],]

    for i in range(len(member_groups) - 1, -1, -1):
        group = member_groups[i]
        for j in range(len(member_groups) - 1, i - 1, -1):
            sub_group = member_groups[j]
            if (sub_group.lft > group.lft and sub_group.rght < group.rght):
                result[j][1] = group.name + '/' + result[j][1]
    return result

def get_members_email(request_user, group_id):
    group = get_group(request_user, group_id)
    K = group_models.Permission.objects.filter(group__tree_id = all_members.tree_id).values('user__email')
    print(K)
    # group_models.Permission.objects.filter(group = all_members, group__lft__gte = all_members.lft, group__rght__lte = all_members.rght).values('user__email')
    return group_models.Permission.objects.filter(group__tree_id = all_members.tree_id).values('user__email')


def add_parent_and_save(form, parent):
    if form.is_valid():
        model = form.save(commit=False)
        model.parent = parent
        model.save()

def handle_invite(request_user, group, email, permission):
    if group.has_permission(request_user, group_models.Permission.SUPER_USER):
        if(group.member_in_tree(email)):
            invited_user = User.objects.get(email = email)
            group.add_member(invited_user, permission)
        else:
            group.add_invitation(request_user, email, permission)
    else:
        PermissionDenied()


def handle_invitation_response(request_user, answer, group_id):
    group = get_group(request_user, group_id)
    invitations = list(group_models.Invitation.objects.filter(email = request_user.email, group = group))
    if(len(invitations) == 1):
        invitation = invitations[0]
        if answer == "1":
            group_models.Permission.objects.create(user = request_user, group = group, permission = invitation.permission)

        group_models.Invitation.objects.filter(id = invitation.id).delete()

    else:
        PermissionDenied("Expected 1 invitation but " + str(len(invitations)) +" invitations found")