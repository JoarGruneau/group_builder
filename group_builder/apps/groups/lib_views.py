import group_builder.apps.groups.models as group_models
from django.core.exceptions import PermissionDenied

def get_tree_info(request):
    if request.method == "GET":
        parent = group_models.Group.objects.get(id = request.GET.get("id", ""))
    else:
        parent = group_models.Group.objects.get(id = request.POST.get("id", ""))

    if parent.has_permission(request.user, group_models.Permission.READ):
        tree = parent.get_descendants(include_self=True)
        return parent, tree
    else:
        raise PermissionDenied()

