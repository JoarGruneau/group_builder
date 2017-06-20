from django.db import models
from django.utils import timezone
from group_builder.apps.mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User

class Group(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def has_permission(self, user, permission_type):
        for perm in list(Permission.objects.filter(user = user, group__tree_id__contains=self.tree_id)):
            print(permission_type)
            print(perm.permission)
            if(self.lft >= perm.group.lft and self.rght <= perm.group.rght and permission_type <= perm.permission):
                return True
        return False


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,)

    READ = 1
    UPLOAD = 2
    SUPER_USER = 3
    permission_choice = ((READ, "read"), (UPLOAD, "upload"), (SUPER_USER, "super_user"))
    permission = models.PositiveIntegerField(choices = permission_choice, default = READ)
