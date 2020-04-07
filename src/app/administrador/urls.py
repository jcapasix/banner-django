from django.conf.urls import include, url
from django.contrib import admin


from . import views

urlpatterns = [
	
	#url(r'^books/$', views.book_list, name='book_list'),

    url(r'^aulas/$', views.aula_list, name='aula_list'),
    url(r'^aulas/create/$', views.aula_create, name='aula_create'),
    url(r'^aulas/(?P<pk>\d+)/update/$', views.aula_update, name='aula_update'),
    url(r'^aulas/(?P<pk>\d+)/delete/$', views.aula_delete, name='aula_delete'),


    url(r'^profesores/$', views.profesor_list, name='profesor_list'),
    url(r'^profesores/create/$', views.profesor_create, name='profesor_create'),
    url(r'^profesores/(?P<pk>\d+)/update/$', views.profesor_update, name='profesor_update'),
    url(r'^profesores/(?P<pk>\d+)/delete/$', views.profesor_delete, name='profesor_delete'),


    #Detalle Profesor Cursos
    url(r'^profesores/(?P<profesor_pk>\d+)/cursos/$', views.profesor_cursos, name='profesor_cursos'), # new
    url(r'^profesores/cursos/(?P<profesor_pk>\d+)/create/$', views.profesor_cursos_create, name='profesor_cursos_create'), # new
    url(r'^profesores/cursos/(?P<pk>\d+)/update/$', views.profesor_cursos_update, name='profesor_cursos_update'), # new
    url(r'^profesores/cursos/(?P<pk>\d+)/delete/$', views.profesor_cursos_delete, name='profesor_cursos_delete'), # new


    url(r'^estudiantes/$', views.estudiante_list, name='estudiante_list'),
    url(r'^estudiantes/create/$', views.estudiante_create, name='estudiante_create'),
    url(r'^estudiantes/(?P<pk>\d+)/update/$', views.estudiante_update, name='estudiante_update'),
    url(r'^estudiantes/(?P<pk>\d+)/delete/$', views.estudiante_delete, name='estudiante_delete'),


    url(r'^apoderados/$', views.apoderado_list, name='apoderado_list'),
    url(r'^apoderados/create/$', views.apoderado_create, name='apoderado_create'),
    url(r'^apoderados/(?P<pk>\d+)/update/$', views.apoderado_update, name='apoderado_update'),
    url(r'^apoderados/(?P<pk>\d+)/delete/$', views.apoderado_delete, name='apoderado_delete'),


    url(r'^cursos/$', views.curso_list, name='curso_list'), # new
    url(r'^cursos/create/$', views.curso_create, name='curso_create'), # new
    url(r'^cursos/(?P<pk>\d+)/update/$', views.curso_update, name='curso_update'), # new
    url(r'^cursos/(?P<pk>\d+)/delete/$', views.curso_delete, name='curso_delete'), # new


    #Detalles
    #url(r'^aula_cursos/$', views.aula_cursos_list, name='aula_cursos_list'), # new

    url(r'^aulas/(?P<aula_pk>\d+)/cursos/$', views.aula_cursos, name='aula_cursos'), # new
    url(r'^aulas/cursos/(?P<aula_pk>\d+)/create/$', views.aula_cursos_create, name='aula_cursos_create'), # new
    url(r'^aulas/cursos/(?P<pk>\d+)/update/$', views.aula_cursos_update, name='aula_cursos_update'), # new
    url(r'^aulas/cursos/(?P<pk>\d+)/delete/$', views.aula_cursos_delete, name='aula_cursos_delete'), # new

    url(r'^aulas/(?P<aula_pk>\d+)/profesores/$', views.aula_profesores, name='aula_profesores'), # new
    url(r'^aulas/profesores/(?P<aula_pk>\d+)/create/$', views.aula_profesores_create, name='aula_profesores_create'), # new
    url(r'^aulas/profesores/(?P<pk>\d+)/update/$', views.aula_profesores_update, name='aula_profesores_update'), # new
    url(r'^aulas/profesores/(?P<pk>\d+)/delete/$', views.aula_profesores_delete, name='aula_profesores_delete'), # new

]
