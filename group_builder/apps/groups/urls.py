from django.conf.urls import url
import group_builder.apps.groups.views as group_views
#import group_builder.apps.groups.forms as group_forms

urlpatterns = [
	url(r'^create/group$', group_views.create_group, name='create_group'),
]
