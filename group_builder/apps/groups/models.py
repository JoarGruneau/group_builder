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

    def field_url(self):
        return "?id="+str(self.id)
    
    def has_permission(self, user, permission_type):
        return Permission.objects.filter(user = user, permission__gte = permission_type,
            group__tree_id=self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).exists()

    def has_invitation(self, email, permission_type):
        return Invitation.objects.filter(email = email, permission = permission_type).exists()

    #This function needs work since it can return the same member with number of times with different permissions
    def get_members(self):
        members = Permission.objects.filter(
            group__tree_id = self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).values(
              'user__first_name', 'user__last_name', 'user__email', 'permission')
        innvited = Invitation.objects.filter(
            group__tree_id = self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).values(
              'email', 'permission')
        #members = User.objects.filter(id=perm.values('user__id'))
        return members, innvited

    def get_all_members(self):
        members = Permission.objects.filter(
            group__tree_id = self.tree_id).values(
            'user__first_name', 'user__last_name', 'user__email').distinct()
        return members

    def member_exsist(self, email):
        return Permission.objects.filter(user__email = email, group__tree_id=self.tree_id).exists()

    def get_documents(self):
        return Document.objects.filter(group__id = self.id)

    def get_events(self):
        return Event.objects.filter(
            group__tree_id = self.tree_id, group__lft__gte = self.lft, group__rght__lte = self.rght)


class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    group = models.OneToOneField(Group, on_delete=models.CASCADE,)

    READ = 1
    UPLOAD = 2
    SUPER_USER = 3
    permission_choice = ((READ, "read"), (UPLOAD, "upload"), (SUPER_USER, "super_user"))
    permission = models.PositiveIntegerField(choices = permission_choice, default = READ)

class Invitation(models.Model):
    email = models.EmailField(max_length=254, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='invited_by')
    permission = models.PositiveIntegerField(choices = Permission.permission_choice, default = Permission.READ)

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Event(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_date = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)
    
