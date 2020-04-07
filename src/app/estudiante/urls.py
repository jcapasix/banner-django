# from django.conf.urls import include, url
# from django.contrib import admin


# from . import views

# urlpatterns = [
	
# 	#url(r'^books/$', views.book_list, name='book_list'),

#     url(r'^asistencias/$', views.asistencia_index, name='asistencia_index'),
#     url(r'^notas/$', views.notas_index, name='notas_index'),
#     url(r'^observaciones/$', views.observaciones_index, name='observaciones_index'),

#     #url(r'^asistencias/create/$', views.aula_create, name='asistencia_create'),
#     #url(r'^asistencias/(?P<pk>\d+)/update/$', views.aula_update, name='asistencia_update'),
#     #url(r'^asistencias/(?P<pk>\d+)/delete/$', views.aula_delete, name='aula_delete'),

# ]

from django.conf.urls import include, url
from django.contrib import admin


from . import views

urlpatterns = [
	
	#url(r'^books/$', views.book_list, name='book_list'),

    # url(r'^change-son/$', views.change_son, name='change_son'),

    url(r'^asistencias/$', views.asistencia_alumnos_list, name='student_asistencia_index'),
    #url(r'^asistencias/(?P<pk>\d+)/$', views.asistencia_alumnos_list, name='student_asistencia_alumnos_list'),
    url(r'^tareas/$', views.tareas_alumnos_list, name='student_tareas_index'),
	#url(r'^tareas/(?P<pk>\d+)/$', views.tareas_alumnos_list, name='tareas_alumnos_list'),


	# url(r'^observaciones/$', views.observaciones_alumnos_list, name='student_observaciones_index'),
    #url(r'^observaciones/(?P<pk>\d+)/$', views.observaciones_alumnos_list, name='observaciones_alumnos_list'),


	url(r'^calificaciones/$', views.calificaciones_index, name='student_calificaciones_index'),
	url(r'^calificaciones/(?P<pk>\d+)/$', views.calificaciones_alumnos_list, name='student_calificaciones_alumnos_list'),

    #url(r'^asistencias/create/$', views.aula_create, name='asistencia_create'),
    #url(r'^asistencias/(?P<pk>\d+)/update/$', views.aula_update, name='asistencia_update'),
    #url(r'^asistencias/(?P<pk>\d+)/delete/$', views.aula_delete, name='aula_delete'),

]
