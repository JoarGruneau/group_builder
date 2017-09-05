from django.conf.urls import url
import group_builder.apps.groups.views as group_views
#import group_builder.apps.groups.forms as group_forms

urlpatterns = [
    url(r'^$', group_views.home, name='home'),
    url(r'^group$', group_views.group, name='group'),
    url(r'^conversations$', group_views.conversations, name='conversations'),
    url(r'^members$', group_views.members, name='members'),
    url(r'^documents$', group_views.documents, name='documents'),
    url(r'^timetables$', group_views.timetables, name='timetables'),
	url(r'^create/group$', group_views.create_group, name='create_group'),
    url(r'^create/child$', group_views.create_child, name='create_child'),
]
