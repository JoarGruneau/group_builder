from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views
import group_builder.apps.accounts.views as accounts_views
import group_builder.apps.accounts.forms as accounts_forms

urlpatterns = [
	url(r'^$', accounts_views.home, name='home'),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': accounts_forms.LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^register/$', accounts_views.register, name='register'),
]
