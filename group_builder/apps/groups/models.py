from django.db import models
from django.utils import timezone
from group_builder.apps.mptt.models import MPTTModel, TreeForeignKey

class Group_Base(MPTTModel):
    creator = models.ForeignKey('auth.User')
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

class Group(MPTTModel):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']
