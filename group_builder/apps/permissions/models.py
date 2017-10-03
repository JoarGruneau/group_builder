from django.db import models
from django.contrib.auth.models import User

import group_builder.apps.groups.models as group_models

class Default_Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,)
    READ = 1
    CONTRIBUTE = 2
    SUPER_USER = 3
    permission_choice = ((READ, "read"), (CONTRIBUTE, "contribute"), (SUPER_USER, "super user"))
    permission = models.PositiveIntegerField(choices = permission_choice, default = READ)

class User_member_type(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    group = models.ForeignKey(Group, on_delete=models.CASCADE,)


# class Document_permission(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     VIEW = 1
#     UPPLOAD = 2
#     COMMENT = 3
#     UPDATE = 4
#     permission_choice = ((VIEW, 'view'), (UPPLOAD, 'uppload'), (COMMENT, 'comment'), (UPDATE, 'update'))
#     permission = models.PositiveIntegerField(choices = permission_choice)


# class Member_permission(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     VIEW = 1
#     EMAIL = 2
#     EXTRA_INFO = 3
#     permission_choice = ((VIEW, 'view'), (EMAIL, 'email'), (EXTRA_INFO, 'extra info'),)
#     permission = models.PositiveIntegerField(choices = permission_choice)

# class Post_permission(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     VIEW = 1
#     REPLY_TO_POST = 2
#     POST = 3
#     permission_choice = ((VIEW, 'view'), (REPLY_TO_POST, 'reply to post'), (POST, 'post'),)
#     permission = models.PositiveIntegerField(choices = permission_choice)

# class Timetable_permission(models.Model):
#     group = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     member_type = models.ForeignKey(Group, on_delete=models.CASCADE,)
#     VIEW = 1
#     permission_choice = ((VIEW, 'view'),)
#     permission = models.PositiveIntegerField(choices = permission_choice)