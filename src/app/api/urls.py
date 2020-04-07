from django.conf.urls import include, url
from django.contrib import admin
#from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet

from app.api import views


urlpatterns = [

	#url(r'^devices?$', FCMDeviceAuthorizedViewSet.as_view({'post': 'create'}), name='create_fcm_device'),
	
	url(r'^auth/', include('djoser.urls.authtoken')),

	url(r'^login/$', views.LoginView.as_view(), name='log'),
	url(r'^changeson/$', views.ChangeSon.as_view()),

	url(r'^sons/$', views.SonList.as_view()),


    #url(r'^asistencias/(?P<pk>[0-9]+)/$', views.AsistenciaDetail.as_view()),
	url(r'^cursos/$', views.DetalleAulaCursoList.as_view()),

	url(r'^asistencias/$', views.AsistenciaList.as_view()),
    url(r'^calificaciones/$', views.CalificacionList.as_view()),
    url(r'^observaciones/$', views.ObservacionList.as_view()),


    url(r'^tareas/$', views.TareaList.as_view()),
    
]
