from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('group_builder.apps.sitetree.urls')),
    url(r'', include('group_builder.apps.accounts.urls')),
    url(r'', include('group_builder.apps.groups.urls')),
]
