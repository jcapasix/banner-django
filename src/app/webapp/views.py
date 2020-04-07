#-*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.template.context import RequestContext
from django.http import HttpResponse,HttpResponseRedirect

#para el sistema de login importamos lo siguiente
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

#from .forms import UserRegisterFrom
#from .models import Tipo
import json
#from django.core import serializers
import time
#from app.db.models import *

def index(request):
	fecha = time.strftime('%Y-%m-%d')
	if not request.user.is_anonymous():
		if request.user.es_administrador:
			colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
			administrador = Administrador.objects.get(user__id = request.user.id)

			colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)

			aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
			_aulas = []
			for aula in aulas:
				d = {'grado': aula.grado.grado,'nivel':aula.nivel.nivel,'seccion':aula.seccion.seccion, 'size':Estudiante.objects.filter(aula=aula).count()}
				_aulas.append(d)

			_aulas = json.dumps(_aulas)

			context = {
			'fecha':fecha,
			'aulas':_aulas, 
			'colegios':colegios,
			'colegio':colegio,
			'page_name':'Pizarra', 
			'administrador':administrador, 
			'pizarra_active':'active',
			'aulas_size':Aula.objects.filter(colegio__id = administrador.colegio_defecto.id).count(),
			'profesores_size':DetalleProfesorColegio.objects.filter(colegio__id = administrador.colegio_defecto.id).count(),
			'estudiantes_size':DetalleEstudianteColegio.objects.filter(colegio__id = administrador.colegio_defecto.id).count(),
			'apoderados_size':DetalleApoderadoColegio.objects.filter(colegio__id = administrador.colegio_defecto.id).count()}

			return render(request, 'administrador/index.html',context)

		if request.user.es_profesor:
			colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
			#profesor nos permite ver el colegio por defecto del profesor
			profesor = Profesor.objects.get(user__id = request.user.id)
			context = {'colegios':colegios,'page_name':'Pizarra', 'profesor':profesor, 'pizarra_active':'active'}
			return render(request, 'profesor/index.html',context)

		if request.user.es_estudiante:
			colegios = DetalleEstudianteColegio.objects.filter(estudiante__user__id=request.user.id)
			estudiante = Estudiante.objects.get(user__id = request.user.id)
			context = {'colegios':colegios,'page_name':'Pizarra', 'estudiante':estudiante, 'pizarra_active':'active'}
			return render(request, 'estudiante/index.html', context)

		if request.user.es_apoderado:
			hijos = Estudiante.objects.filter(apoderado__user__id=request.user.id)
			apoderado = Apoderado.objects.get(user__id = request.user.id)
			hijo_defecto = Estudiante.objects.get(user__username=apoderado.hijo_defecto)

			asistencias = Asistencia.objects.filter(estudiante=hijo_defecto, estado=1).count()
			faltas = Asistencia.objects.filter(estudiante=hijo_defecto, estado=3).count()
			tardanzas = Asistencia.objects.filter(estudiante=hijo_defecto, estado=2).count()

			context = {'hijos':hijos,
			'fecha':fecha,
			'page_name':'Pizarra', 
			'apoderado':apoderado,
			'hijo_defecto':hijo_defecto, 
			'pizarra_active':'active',
			'asistencias':asistencias,
			'faltas':faltas,
			'tardanzas':tardanzas}
			return render(request, 'apoderado/index.html', context)


	return render(request, 'index.html',)




#para los forms
from .forms import *
from django.forms.formsets import formset_factory
#from django.core.context_processors import csrf


@login_required(login_url='/')
def aulas(request):
	if request.user.is_superuser:
		context = {'title_page': 'Aulas'}
		aulas = Aula.objects.all()

		if request.POST:
			#esta para corregir 
			form = AulaForm(request.POST)
			if form.is_valid():
				aula = form.save(commit=False)
				aula.usuario = request.user
				aula.save()

				return HttpResponseRedirect('/administrador/aulas')
		else:
			form = AulaForm()
		args = {}
		args.update(csrf(request))
		args['form'] = form

		template = "administrator/aulas.html"
		return render(request, template , context)
	return redirect('/')

@login_required(login_url='/')
def estudiantes(request):
	if request.user.is_superuser:
		context = {'title_page': 'Estudiantes'}
		estudiantes = Estudiante.objects.all()

		if request.POST:
			#esta para corregir 
			form = EstudianteForm(request.POST)
			if form.is_valid():
				estudiante = form.save(commit=False)
				#estudiante.usuario = request.user
				estudiante.save()

				return HttpResponseRedirect('/administrador/estudiantes')
		else:
			form = EstudianteForm()
		args = {}
		args.update(csrf(request))
		args['form'] = form

		template = "administrator/estudiantes.html"
		return render(request, template , context)
	return redirect('/')



@login_required(login_url='/')
def apoderados(request):
	if request.user.is_superuser:
		context = {'title_page': 'Apoderados'}
		#aulas = Aula.objects.all()
		#niveles = Nivel.objects.all()
		#profesores = Profesor.objects.all()
		apoderados = Apoderado.objects.all()

		if request.POST:
			#esta para corregir 
			form = ApoderadoForm(request.POST)
			if form.is_valid():
				apoderado = form.save(commit=False)
				apoderado.usuario = request.user
				apoderado.save()

				return HttpResponseRedirect('/administrador/apoderados')
		else:
			form = ApoderadoForm()
		args = {}
		args.update(csrf(request))
		args['form'] = form

		template = "administrator/apoderados.html"
		return render(request, template , context)		
	return redirect('/')


@login_required(login_url='/')
def profesores(request):
	if request.user.is_superuser:
		context = {'title_page': 'Profesores'}
		profesores = Profesor.objects.all()

		if request.POST:
			#esta para corregir 
			form = ProfesorForm(request.POST)
			if form.is_valid():
				profesor = form.save(commit=False)
				#profesor.usuario = request.user
				profesor.save()
				return HttpResponseRedirect('/administrador/profesores')
		else:
			form = ProfesorForm()
		args = {}
		args.update(csrf(request))
		args['form'] = form

		template = "administrator/profesores.html"
		return render(request, template , context)
	return redirect('/')
	


@login_required(login_url='/')
def board_administrador(request):
	if request.user.es_profesor:
		return redirect('/board/profesor')
	elif request.user.es_apoderado:
		return redirect('/board/apoderado')
	elif request.user.es_estudiante:
		return redirect('/board/estudiante')
	elif request.user.is_superuser:
		template = "boards/board_administrador.html"
		return render(request, template)



#Vistas del Profesor
'''@login_required(login_url='/')
def board_profesor(request):
	context = {'title_page': 'Profesor'}
	template = "boards/board_profesor.html"
	return render(request, template , context)

@login_required(login_url='/')
def board_profesor_aulas(request):
	context = {'title_page': 'Profesor'}
	template = "profesor/aulas.html"
	return render(request, template , context)

@login_required(login_url='/')
def board_profesor_asistencia(request):
	context = {'title_page': 'Profesor'}
	template = "profesor/asistencia.html"
	return render(request, template , context)

@login_required(login_url='/')
def board_estudiante(request):
	context = {'title_page': 'Estudiante'}
	template = "boards/board_estudiante.html"
	return render(request, template , context)


@login_required(login_url='/')
def board_apoderado(request):
	context = {'title_page': 'Apoderado'}
	template = "boards/board_apoderado.html"
	return render(request, template , context)'''



@login_required(login_url='/')
def salir(request):
	logout(request)
	return redirect('/')


def LogIn(request, username, password):
	user = authenticate( username = username, password = password)
	if user is not None:
		if user.is_active:
			login(request, user)



def pizarra(request):
	"""A view of all bands."""
	return render(request, 'index.html',)
