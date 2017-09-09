import group_builder.apps.groups.models as group_models
from django.core.exceptions import PermissionDenied

def get_all_groups(request):
    permissions = group_models.Permission.objects.filter(user = request.user)
    groups = []
    for permission in permissions:
        groups = groups + list(permission.group.get_descendants(include_self=True))
    return groups

def get_tree_info(request, group_id):
    parent = group_models.Group.objects.get(id = group_id)
    if parent.has_permission(request.user, group_models.Permission.READ):
        tree = parent.get_descendants(include_self=True)
        return parent, tree
    else:
        raise PermissionDenied()

def add_parent_and_save(form, parent):
    if form.is_valid():
        model = form.save(commit=False)
        model.parent = parent
        model.save()