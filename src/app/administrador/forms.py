#-*- coding: utf-8 -*-
from django import forms
from app.db.models import *

class UserLoginFrom(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','password')

class AulaForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(AulaForm, self).__init__(*args, **kwargs)
		self.fields['nivel'].label = 'Nivel:'
		self.fields['grado'].label = 'Grado:'
		self.fields['seccion'].label = 'Sección:'
	class Meta:
		model = Aula
		fields = ('nivel', 'grado', 'seccion')


class CursoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(CursoForm, self).__init__(*args, **kwargs)
		self.fields['nombre'].label = 'Nombre:'
		self.fields['descripcion'].label = 'Descripción:'
	class Meta:
		model = Curso
		fields = ('nombre', 'descripcion',)


class UserForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'DNI:'
		self.fields['first_name'].label = 'Nombre:'
		self.fields['last_name'].label = 'Apellidos:'
		self.fields['email'].label = 'Correo:'
	class Meta:
		model = User
		fields = ('username','first_name','last_name', 'email', 'genero')


class ProfesorForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfesorForm, self).__init__(*args, **kwargs)
		self.fields['profesion'].label = 'Profesión:'
		self.fields['telefono'].label = 'Teléfono:'
		self.fields['hobby'].label = 'Hobby:'
	class Meta:
		model = Profesor
		fields = ('profesion', 'telefono', 'hobby',)


class EstudianteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(EstudianteForm, self).__init__(*args, **kwargs)
		self.fields['aula'].label = 'Aula:'
		self.fields['telefono'].label = 'Teléfono:'
		self.fields['apoderado'].label = 'Apoderado:'
	class Meta:
		model = Estudiante
		fields = ('aula', 'telefono', 'apoderado',)

class ApoderadoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(ApoderadoForm, self).__init__(*args, **kwargs)
		self.fields['telefono'].label = 'Teléfono:'
	class Meta:
		model = Apoderado
		fields = ('telefono',)

#news
class DetalleAulaCursoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(DetalleAulaCursoForm, self).__init__(*args, **kwargs)
		self.fields['curso'].label = 'Curso:'
	class Meta:
		model = DetalleAulaCurso
		fields = ('curso',)

class DetalleAulaProfesorForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(DetalleAulaProfesorForm, self).__init__(*args, **kwargs)
		self.fields['profesor'].label = 'Profesor:'
	class Meta:
		model = DetalleAulaProfesor
		fields = ('profesor',)

class DetalleProfesorCursoForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(DetalleProfesorCursoForm, self).__init__(*args, **kwargs)
		self.fields['curso'].label = 'Curso:'
	class Meta:
		model = DetalleProfesorCurso
		fields = ('curso',)
		#exclude = ('profesor','is_active')

