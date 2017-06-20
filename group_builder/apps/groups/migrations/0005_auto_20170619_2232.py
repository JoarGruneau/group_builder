# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 22:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0004_auto_20170619_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='level',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='group',
            name='lft',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='rght',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='group',
            name='tree_id',
            field=models.PositiveIntegerField(default=0),
        ),
    ]