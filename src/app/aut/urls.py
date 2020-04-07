from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

	#url(r'^login/$', views.login_view, name='login'),
    url(r'^login/$', auth_views.login, name='ingresar', kwargs={'template_name': 'index.html'}),
    url(r'^logout/$', views.logout_view, name='salir'),
	#url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
]


