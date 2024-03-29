from django.conf.urls import url
import group_builder.apps.groups.views as group_views
#import group_builder.apps.groups.forms as group_forms

urlpatterns = [
    url(r'^$', group_views.home, name='home'),
    url(r'^invitations$', group_views.invitations, name='invitations'),
    url(r'^invitations/response/(?P<answer>[0-1])/(?P<group_id>[0-9]*)$', group_views.invitation_response, name='invitation_response'),
    url(r'^group/(?P<group_id>[0-9]*)$', group_views.group, name='group'),
    url(r'^overview/(?P<group_id>[0-9]*)$', group_views.group, name='overview'),
    url(r'^members/(?P<group_id>[0-9]*)$', group_views.members, name='members'),
    url(r'^members/(?P<group_id>[0-9]*)/add$', group_views.add_members, name='add_members'),
    url(r'^documents/(?P<group_id>[0-9]*)$', group_views.documents, name='documents'),
    url(r'^posts/(?P<group_id>[0-9]*)$', group_views.posts, name='posts'),
    url(r'^chat/(?P<group_id>[0-9]*)$', group_views.posts, name='chat'),
    url(r'^timetables/(?P<group_id>[0-9]*)$', group_views.timetables, name='timetables'),
	url(r'^create/group$', group_views.create_group, name='create_group'),
    url(r'^create/child/(?P<group_id>[0-9]*)$', group_views.create_child, name='create child'),
    url(r'^create/event/(?P<group_id>[0-9]*)$', group_views.create_event, name='create_event'),
    url(r'^api/get_email_addresses/(?P<group_id>[0-9]*)$', group_views.get_email_addresses),
]
