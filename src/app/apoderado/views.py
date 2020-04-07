#-*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from app.db.models import *
#from django.core.context_processors import csrf

#from .forms import *

from django.http import JsonResponse
from django.template.loader import render_to_string

import time
@login_required(login_url='/')
def asistencia_alumnos_list(request):
	if request.user.es_apoderado and not request.user.is_anonymous():
		hijos = Estudiante.objects.filter(apoderado__user__id=request.user.id)
		apoderado = Apoderado.objects.get(user__id = request.user.id)
		hijo_defecto = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
		if request.method == 'GET':
			fecha =  request.GET.get('fecha')
			apoderado = Apoderado.objects.get(user=request.user)
			estudiante = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
			try:
				if fecha is not None:
					is_asistencias = True
					_asistencias = Asistencia.objects.filter(estudiante=estudiante, fecha=fecha)
				else:
					fecha = time.strftime('%Y-%m-%d')
					is_asistencias = True
					_asistencias = Asistencia.objects.filter(estudiante=estudiante, fecha=fecha)

				colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
				context = {
				'is_asistencias':is_asistencias, 
				'asistencias':_asistencias, 
				'page_name':'Asistencia', 
				'asistencia_active':'active',
				'fecha':fecha,
				'hijos':hijos,
				'hijo_defecto':hijo_defecto}
				return render(request, 'apoderado/asistencias/asistencia_alumnos_list.html', context)

			except AsistenciaAula.DoesNotExist:

				#falta optimizar
				profesor = Profesor.objects.get(user__id = request.user.id)
				detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=aula_pk, colegio__id = profesor.colegio_defecto.id)
				estudiantes = getListDetalleEstudiantes(detalle_estudiante)

				colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
				context = {
				'is_asistencias':is_asistencias, 
				'asistencias':_asistencias, 
				'estudiantes':estudiantes, 
				'profesor':profesor, 
				'page_name':'Asistencia', 
				'colegios':colegios, 
				'asistencia_active':'active',
				'fecha':fecha,
				'is_save':is_save,
				'detalle':detalle,
				'hijos':hijos,
				'hijo_defecto':hijo_defecto}
				return render(request, 'apoderado/asistencias/asistencia_alumnos_list.html', context)
	else:
		return redirect('/')



#CALIFICACIONES 
@login_required(login_url='/')
def calificaciones_index(request):

	if request.user.es_apoderado and not request.user.is_anonymous():
		hijos = Estudiante.objects.filter(apoderado__user__id=request.user.id)
		apoderado = Apoderado.objects.get(user__id = request.user.id)
		hijo_defecto = Estudiante.objects.get(user__username=apoderado.hijo_defecto)

		estudiante = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
		detalles = DetalleAulaCurso.objects.filter(aula=estudiante.aula)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'detalles':detalles, 
		'apoderado':apoderado, 
		'page_name':'Asistencia', 
		'colegios':colegios, 
		'calificaciones_active':'active',
		'hijos':hijos,
		'hijo_defecto':hijo_defecto,
		'apoderado':apoderado}
		return render(request, 'apoderado/calificaciones/calificaciones.html', context)
	else:
		return redirect('/')


from django.core import serializers
@login_required(login_url='/')
def calificaciones_alumnos_list(request, pk):
	if request.user.es_apoderado and not request.user.is_anonymous():
		curso = Curso.objects.get(id=pk)
		hijos = Estudiante.objects.filter(apoderado__user__id=request.user.id)
		apoderado = Apoderado.objects.get(user__id = request.user.id)
		hijo_defecto = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
		estudiante = Estudiante.objects.get(user__username = apoderado.hijo_defecto)
		estudiante.notas = Calificacion.objects.filter(estudiante__id=estudiante.id, curso=curso)
		context = {'estudiante':estudiante, 
		'page_name':'Calificaciones', 
		'calificaciones_active':'active',
		'hijos':hijos,
		'hijo_defecto':hijo_defecto,
		'apoderado':apoderado}
		return render(request, 'apoderado/calificaciones/calificaciones_alumnos_list.html', context)
	else:
		return redirect('/')


@login_required(login_url='/')
def observaciones_alumnos_list(request):

	if request.user.es_apoderado and not request.user.is_anonymous():
		hijos = Estudiante.objects.filter(apoderado__user__id=request.user.id)
		apoderado = Apoderado.objects.get(user__id = request.user.id)
		hijo_defecto = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
		estudiante = Estudiante.objects.get(user__username = apoderado.hijo_defecto)
		estudiante.observaciones = Observacion.objects.filter(estudiante__id=estudiante.id)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'estudiante':estudiante, 
		'page_name':'Observaciones', 
		'colegios':colegios, 
		'observaciones_active':'active',
		'hijos':hijos,
		'hijo_defecto':hijo_defecto,
		'apoderado':apoderado}
		return render(request, 'apoderado/observaciones/observaciones_alumnos_list.html', context)
	else:
		return redirect('/')




#TAREAS
@login_required(login_url='/')
def tareas_alumnos_list(request):
	if request.user.es_apoderado and not request.user.is_anonymous():
		hijos = Estudiante.objects.filter(apoderado__user__id=request.user.id)
		apoderado = Apoderado.objects.get(user__id = request.user.id)
		hijo_defecto = Estudiante.objects.get(user__username=apoderado.hijo_defecto)

		apoderado = Apoderado.objects.get(user__id = request.user.id)
		estudiante = Estudiante.objects.get(user__username = apoderado.hijo_defecto)
	
		tareas = Tarea.objects.filter(aula__id=estudiante.aula.id)
		tareas = serializers.serialize("json", tareas)

		#falta optimizar
		#detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=pk, colegio__id = profesor.colegio_defecto.id)
		#estudiantes = getListDetalleEstudiantes(detalle_estudiante)

		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		cursos = Curso.objects.all()
		context = {'cursos':cursos,
		'tareas':tareas, 
		'page_name':'Tareas', 
		'colegios':colegios, 
		'tareas_active':'active',
		'hijos':hijos,
		'apoderado':apoderado,
		'hijo_defecto':hijo_defecto}
		return render(request, 'apoderado/tareas/tareas_alumnos_list.html', context)
	else:
		return redirect('/')




def getListDetalleEstudiantes(obj):
	nuewObj = list()
	for e in obj:
		nuewObj.append(e.estudiante)
	return nuewObj


@login_required(login_url='/')
def change_son(request):
	if request.user.es_apoderado and not request.user.is_anonymous():
		if request.method == 'POST':
			estudiante_username = request.POST.get('estudiante_username')
			apoderado = Apoderado.objects.get(user__id = request.user.id)
			apoderado.hijo_defecto = estudiante_username
			apoderado.save()
			return redirect('/')
	else:
		return redirect('/')




