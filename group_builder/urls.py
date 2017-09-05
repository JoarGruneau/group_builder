from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from group_builder.settings import dev

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('group_builder.apps.accounts.urls')),
    url(r'', include('group_builder.apps.groups.urls')),
] + static(dev.MEDIA_URL, document_root=dev.MEDIA_ROOT)
