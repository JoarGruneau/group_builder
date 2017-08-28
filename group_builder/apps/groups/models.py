from django.db import models
from django.utils import timezone
from group_builder.apps.mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Group(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def has_permission(self, user, permission_type):
        if(Permission.objects.filter(
            user = user, group__tree_id=self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).exists()):
            return True
        else:
            return False

    def field_url(self):
        return "?id="+str(self.id)

    def get_members(self):
        members = Permission.objects.filter(
            group__tree_id = self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).values(
            'user__first_name', 'user__last_name', 'user__email', 'permission')
        #members = User.objects.filter(id=perm.values('user__id'))
        return list(members)



class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    group = models.OneToOneField(Group, on_delete=models.CASCADE,)

    READ = 1
    UPLOAD = 2
    SUPER_USER = 3
    permission_choice = ((READ, "read"), (UPLOAD, "upload"), (SUPER_USER, "super_user"))
    permission = models.PositiveIntegerField(choices = permission_choice, default = READ)


class Invitations(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='invited_by')
    permission = models.PositiveIntegerField(choices = Permission.permission_choice, default = Permission.READ)