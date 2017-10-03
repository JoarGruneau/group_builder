import os
from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Group(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    DEFAULT = 0
    MEMBER_GROUP = 1
    MEMBER_SUB = 2
    ONE__MANY = 3
    SPECIAL_ACCESS = 4
    group_choices = ((DEFAULT, "default"), (MEMBER_GROUP, "all members"), (MEMBER_SUB, "members"), 
        (ONE__MANY, "one to many"), (SPECIAL_ACCESS, "special access"))
    group_type = models.PositiveIntegerField(choices = group_choices, default = DEFAULT)

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_rooms(self):
        return Group_room.objects.filter(group = self)
    
    def has_permission(self, user, permission_type):
        return Permission.objects.filter(user = user, permission__gte = permission_type,
            group__tree_id=self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).exists()

    #This function needs work since it can return the same member with number of times with different permissions
    def get_members(self):
        members = Permission.objects.filter(
            group__tree_id = self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).values(
              'user__first_name', 'user__last_name', 'user__email')
        default_innvited = Default_invitation.objects.filter(
            group__tree_id = self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).values(
              'email',)
        custom_ivited = Custom_invitation.objects.filter(
            group__tree_id = self.tree_id, group__lft__lte = self.lft, group__rght__gte = self.rght).values(
              'email',)
        invited = list(default_innvited) + list(custom_ivited)
        return members, invited

    def get_member_types(self):
        all_members = Group.objects.get( tree_id = self.tree_id, name ="all members")
        return all_members.get_descendants

    def get_all_members(self):
        members = Permission.objects.filter(
            group__tree_id = self.tree_id).values(
            'user__first_name', 'user__last_name', 'user__email').distinct()
        return members

    def member_in_tree(self, email):
        perms = self.get_descendants(include_self = True)
        return Permission.objects.filter(user__email = email, group__tree_id=self.tree_id).exists()

    def add_member(self, user, permission):
        Permission.objects.filter(user = user, group__tree_id=self.tree_id, group__lft__gte = self.lft, group__rght__lte = self.rght, permission__lte = permission).delete()
        Permission.objects.create(user = user, group = self, permission = permission)

    def get_documents(self):
        return Document.objects.filter(group__id = self.id)

    def get_events(self):
        return Event.objects.filter(
            group__tree_id = self.tree_id, group__lft__gte = self.lft, group__rght__lte = self.rght)

class Group_room(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE,)
    choices = ((1,"overview"), (2, "posts"), (3, "chat"), (4, "documents"), (5, "timetables"))
    room = models.IntegerField(choices = choices)

class Group_member_type():
    group = models.ForeignKey(Group, on_delete=models.CASCADE,)
    member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,)
    READ = 1
    CONTRIBUTE = 2
    SUPER_USER = 3
    permission_choice = ((READ, "read"), (CONTRIBUTE, "contribute"), (SUPER_USER, "super user"),)
    permission = models.PositiveIntegerField(choices = permission_choice)

class Default_invitation(models.Model):
    email = models.EmailField(max_length=254, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='default_invited_by')
    member_type = models.PositiveIntegerField(choices = Permission.permission_choice)


class Custom_invitation(models.Model):
    email = models.EmailField(max_length=254, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    invited_by = models.ForeignKey(User, on_delete = models.CASCADE, related_name='custom_invited_by')
    member_type = models.ForeignKey(Group, on_delete = models.CASCADE, related_name = 'custom_member_type')

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    uploaded = models.DateTimeField(default=timezone.now)
    last_eddited = models.DateTimeField(default=timezone.now, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def filename(self):
        return os.path.basename(self.docfile.name)

class Event(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_date = models.CharField(max_length=100)
    start_time = models.CharField(max_length=100)
    end_date = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)

class Post(models.Model):
    replies_to = models.ForeignKey('self', on_delete=models.CASCADE, null = True)
    sender = models.ForeignKey(User)
    time = models.DateTimeField(default=timezone.now)
    message =  models.TextField()

class Document_permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name = 'document_group')
    member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
    VIEW = 1
    UPPLOAD = 2
    COMMENT = 3
    UPDATE = 4
    permission_choice = ((VIEW, 'view'), (UPPLOAD, 'uppload'), (COMMENT, 'comment'), (UPDATE, 'update'))
    permission = models.PositiveIntegerField(choices = permission_choice)


class Member_permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name = 'member_group')
    member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
    VIEW = 1
    EMAIL = 2
    EXTRA_INFO = 3
    permission_choice = ((VIEW, 'view'), (EMAIL, 'email'), (EXTRA_INFO, 'extra info'),)
    permission = models.PositiveIntegerField(choices = permission_choice)

class Post_permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name = 'post_group')
    member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
    VIEW = 1
    REPLY_TO_POST = 2
    POST = 3
    permission_choice = ((VIEW, 'view'), (REPLY_TO_POST, 'reply to post'), (POST, 'post'),)
    permission = models.PositiveIntegerField(choices = permission_choice)

class Timetable_permission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name = 'timtable_group')
    member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
    VIEW = 1
    permission_choice = ((VIEW, 'view'),)
    permission = models.PositiveIntegerField(choices = permission_choice)
    
