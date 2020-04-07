#-*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from app.db.models import *
#from django.core.context_processors import csrf

from .forms import *

from django.http import JsonResponse
from django.template.loader import render_to_string


def asistencia_index(request):
	if request.user.is_anonymous():
		return redirect('/')
	if request.user.es_profesor:
		profesor = Profesor.objects.get(user__id = request.user.id)
		detalles = DetalleProfesorCurso.objects.filter(profesor=profesor)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'detalles':detalles, 'profesor':profesor, 'page_name':'Asistencia', 'colegios':colegios, 'asistencia_active':'active'}
		return render(request, 'profesor/asistencias/aulas.html', context)
	else:
		return redirect('/')


from django.core.serializers import serialize
import json
import time


def asistencia_alumnos_list(request, pk):
	is_save = 0
	is_asistencias = False
	_asistencias = None

	detalle = DetalleProfesorCurso.objects.get(pk=pk)
	aula_pk = detalle.curso.aula.id
	curso_pk = detalle.curso.curso.id

	if request.user.es_profesor:

		if request.method == 'GET':
			fecha =  request.GET.get('fecha')
			try:
				if fecha is not None:
					asistencias = AsistenciaAula.objects.get(aula=aula_pk, curso__id=curso_pk, fecha=fecha)
					is_asistencias = True
					profesor = Profesor.objects.get(user__id = request.user.id)
					detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=aula_pk, colegio__id = profesor.colegio_defecto.id)
					estudiantes = getListDetalleEstudiantes(detalle_estudiante)
					_asistencias = Asistencia.objects.filter(aula=aula_pk, curso=curso_pk, fecha=fecha)
				else:
					fecha = time.strftime('%Y-%m-%d')
					asistencias = AsistenciaAula.objects.get(aula__id=aula_pk, curso__id=curso_pk, fecha=fecha)
					is_asistencias = True
					profesor = Profesor.objects.get(user__id = request.user.id)
					detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=aula_pk, colegio__id = profesor.colegio_defecto.id)
					estudiantes = getListDetalleEstudiantes(detalle_estudiante)
					_asistencias = Asistencia.objects.filter(aula=aula_pk, curso=curso_pk, fecha=fecha)

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
				'detalle':detalle}
				return render(request, 'profesor/asistencias/asistencia_alumnos_list.html', context)

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
				'detalle':detalle}
				return render(request, 'profesor/asistencias/asistencia_alumnos_list.html', context)

		if request.method == 'POST':
			try:
				fecha =  request.POST.get('fecha')
				
				#CAPA
				asistencias = AsistenciaAula.objects.get(aula=aula_pk, curso=curso_pk, fecha=fecha)
				alumnos =  json.loads(request.POST.get('obj'))
				
				for alumno in alumnos:
					_id = alumno['id']
					_state = alumno['state']
					estudiante = Estudiante.objects.get(id=_id)
					aula = Aula.objects.get(id=aula_pk)
					curso = Curso.objects.get(id=curso_pk)
					asistencia = Asistencia.objects.get(estudiante=estudiante, aula=aula, curso=curso, fecha=fecha)
					asistencia.estado = _state
					asistencia.save()
					is_save = 1				
				return redirect('/teacher/asistencias/%s/?fecha=%s' % (detalle.id, fecha))

			except AsistenciaAula.DoesNotExist:
				alumnos =  json.loads(request.POST.get('obj'))
				#fecha =  request.POST.get('fecha')
				#creamos las asistencias alumno por alumno
				for alumno in alumnos:
					_id = alumno['id']
					_state = alumno['state']
					estudiante = Estudiante.objects.get(id=_id)
					aula = Aula.objects.get(id=aula_pk)
					curso = Curso.objects.get(id=curso_pk)
					asistencia = Asistencia(estudiante=estudiante, curso=curso, aula=aula, estado=_state, fecha=fecha)
					asistencia.save()
					is_save = 1	
				asistencias = None
				profesor = Profesor.objects.get(user__id = request.user.id)
				aula = Aula.objects.get(id=aula_pk, colegio__id = profesor.colegio_defecto.id)
				curso = Curso.objects.get(id=curso_pk)
				asistencia_aula = AsistenciaAula(aula=aula, 
					turno=1, 
					curso=curso,
					fecha=fecha)
				asistencia_aula.save()
				return redirect('/teacher/asistencias/%s/?fecha=%s' % (detalle.id, fecha))
	else:
		return redirect('/')



#CALIFICACIONES 

def calificaciones_index(request):
	if request.user.is_anonymous():
		return redirect('/')
	if request.user.es_profesor:
		profesor = Profesor.objects.get(user__id = request.user.id)
		detalles = DetalleProfesorCurso.objects.filter(profesor=profesor)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'detalles':detalles, 'profesor':profesor, 'page_name':'Calificaciones', 'colegios':colegios, 'calificaciones_active':'active'}
		return render(request, 'profesor/calificaciones/calificaciones.html', context)
	else:
		return redirect('/')


from django.core import serializers
def calificaciones_alumnos_list(request, pk):
	detalle = DetalleProfesorCurso.objects.get(pk=pk)
	aula_pk = detalle.curso.aula.id
	curso_pk = detalle.curso.curso.id
	if request.user.es_profesor:

		if request.method == 'POST':

			e_dni = request.POST.get('estudiante')
			estudiante = Estudiante.objects.get(user__username = e_dni)
			profesor = Profesor.objects.get(user__id = request.user.id)
			#curso = Curso.objects.get(id = request.POST.get('curso'))
			curso = Curso.objects.get(id=curso_pk)
			nota = request.POST.get('nota')
			descripcion = request.POST.get('descripcion')

			calificacion = Calificacion(estudiante=estudiante, 
				profesor=profesor, 
				curso=curso, 
				nota=nota, 
				descripcion=descripcion)
			calificacion.save()
			return redirect('/teacher/calificaciones/%s/' % pk)


		profesor = Profesor.objects.get(user__id = request.user.id)
		#falta optimizar
		detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=aula_pk, colegio__id = profesor.colegio_defecto.id)
		estudiantes = getListDetalleEstudiantes(detalle_estudiante)
		
		for e in estudiantes:
			e.notas = Calificacion.objects.filter(profesor__user__id=request.user.id,
				estudiante__id=e.id)
			for n in e.notas:
				if n.nota <= 10:
					n.color = "danger"
				else:
					n.color = "success"


		alumnos_json = serializers.serialize("json", estudiantes)


		cursos = Curso.objects.all()

		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'cursos':cursos, 
		'estudiantes':estudiantes,
		'alumnos_json':alumnos_json, 
		'profesor':profesor, 
		'page_name':'Calificaciones', 
		'colegios':colegios, 
		'calificaciones_active':'active',
		'detalle':detalle}
		return render(request, 'profesor/calificaciones/calificaciones_alumnos_list.html', context)
	else:
		return redirect('/')


def observaciones_index(request):
	if request.user.is_anonymous():
		return redirect('/')
	if request.user.es_profesor:
		profesor = Profesor.objects.get(user__id = request.user.id)
		detalles = DetalleProfesorCurso.objects.filter(profesor=profesor)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'detalles':detalles, 
		'profesor':profesor, 
		'page_name':'Observaciones', 
		'colegios':colegios, 
		'observaciones_active':'active'}
		return render(request, 'profesor/observaciones/observaciones.html', context)
	else:
		return redirect('/')

def observaciones_alumnos_list(request, pk):
	detalle = DetalleProfesorCurso.objects.get(pk=pk)
	aula_pk = detalle.curso.aula.id
	curso_pk = detalle.curso.curso.id

	if request.user.es_profesor:
		if request.method == 'POST':
			e_dni = request.POST.get('estudiante')
			estudiante = Estudiante.objects.get(user__username = e_dni)
			profesor = Profesor.objects.get(user__id = request.user.id)
			descripcion = request.POST.get('descripcion')
			curso = Curso.objects.get(id=curso_pk)
			observacion = Observacion(estudiante=estudiante, 
				profesor=profesor,
				descripcion=descripcion,
				curso=curso)
			observacion.save()
			return redirect('/teacher/observaciones/%s/' % pk)

		profesor = Profesor.objects.get(user__id = request.user.id)
		#falta optimizar
		detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=aula_pk, colegio__id = profesor.colegio_defecto.id)
		estudiantes = getListDetalleEstudiantes(detalle_estudiante)
		for e in estudiantes:
			e.observaciones = Observacion.objects.filter(profesor__user__id=request.user.id,
				estudiante__id=e.id)


		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'estudiantes':estudiantes, 
		'profesor':profesor, 
		'page_name':'Observaciones', 
		'colegios':colegios, 
		'observaciones_active':'active',
		'detalle':detalle}
		return render(request, 'profesor/observaciones/observaciones_alumnos_list.html', context)
	else:
		return redirect('/')




#TAREAS
def tareas_index(request):
	if request.user.is_anonymous():
		return redirect('/')
	if request.user.es_profesor:
		profesor = Profesor.objects.get(user__id = request.user.id)
		detalles = DetalleProfesorCurso.objects.filter(profesor=profesor)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'detalles':detalles, 'profesor':profesor, 'page_name':'Tareas', 'colegios':colegios, 'tareas_active':'active'}
		return render(request, 'profesor/tareas/tareas.html', context)
	else:
		return redirect('/')

def tareas_alumnos_list(request, pk):
	detalle = DetalleProfesorCurso.objects.get(pk=pk)
	aula_pk = detalle.curso.aula.id
	curso_pk = detalle.curso.curso.id

	if request.user.es_profesor:

		if request.method == 'POST':
			profesor = Profesor.objects.get(user__id = request.user.id)
			aula = Aula.objects.get(id = aula_pk)
			curso = Curso.objects.get(id = curso_pk)
			title = request.POST.get('title')
			start = request.POST.get('start')
			end = request.POST.get('end')
			detail = request.POST.get('detail')
			
			tarea = Tarea(profesor=profesor,
				aula=aula,
				curso=curso,
				title=title,
				start=start,
				end=end,
				detail=detail)
			tarea.save()

			return redirect('/teacher/tareas/%s/' % pk)

		profesor = Profesor.objects.get(user__id = request.user.id)
		tareas = Tarea.objects.filter(aula__id=aula_pk, profesor__user__id = request.user.id)

		tareas = serializers.serialize("json", tareas)

		#falta optimizar
		detalle_estudiante = DetalleEstudianteColegio.objects.filter(estudiante__aula__id=pk, colegio__id = profesor.colegio_defecto.id)
		estudiantes = getListDetalleEstudiantes(detalle_estudiante)

		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		cursos = Curso.objects.all()
		context = {'estudiantes':estudiantes, 
		'profesor':profesor, 
		'cursos':cursos,
		'tareas':tareas, 
		'page_name':'Tareas', 
		'colegios':colegios, 
		'tareas_active':'active',
		'detalle':detalle}
		return render(request, 'profesor/tareas/tareas_alumnos_list.html', context)
	else:
		return redirect('/')




def getListDetalleEstudiantes(obj):
	nuewObj = list()
	for e in obj:
		nuewObj.append(e.estudiante)
	return nuewObj

