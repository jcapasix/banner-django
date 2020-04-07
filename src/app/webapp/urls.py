from django.conf.urls import include, url
from django.contrib import admin


from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    #url(r'^$', auth_views.login, {'template_name': 'myapp/login.html'}),

]
