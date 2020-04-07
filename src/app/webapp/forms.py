#-*- coding: utf-8 -*-
from django import forms
from app.db.models import *



class UserLoginFrom(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','password')
		widgets = {
			'username': forms.TextInput(attrs = 
				{
				'type':'numeric',
				'class':'form-control',
				'required':'',
				'title':'Introduce tu DNI.',
				'placeholder': 'Introduce tu DNI',
				'autofocus':''
				}),
			'password': forms.TextInput(attrs = 
				{ 
				'type':'password',
				'class':'form-control',
				'required':'',
				'title':'Introduce tu Contraseña',
				'placeholder': 'Introduce tu Contraseña',
				})
		}


class AulaForm(forms.ModelForm):
	class Meta:
		model = Aula
		fields = ('colegio', 'nivel','grado')
		widgets = {
			'nivel': forms.Select(attrs = 
				{
				'required':'',
				'title':'Seleccione un Nivel.',
				}),
			'grado': forms.Select(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Seleccione un Grado.',
				}),

			'profesor': forms.Select(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Seleccione un Profesor.',
				}),
		}

class ProfesorForm(forms.ModelForm):
	class Meta:
		model = Profesor
		fields = ('user','dni','hobby', 'telefono', 'foto')
		widgets = {
			'user': forms.Select(attrs = 
				{
				'required':'',
				'title':'Seleccione el Usuario.',
				}),
			'dni': forms.NumberInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Ingrese su DNI.',
				}),

			'hobby': forms.TextInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				}),
			'telefono': forms.NumberInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Ingrese su Telefono.',
				'autofocus':''
				}),
			'foto': forms.FileInput(attrs = 
				{
				'class':'form-control',
				'title':'Ingrese su foto',
				'autofocus':''
				}),
		}

class EstudianteForm(forms.ModelForm):
	class Meta:
		model = Estudiante
		fields = ('user','aula','apoderado','dni','hobby', 'telefono', 'foto')
		widgets = {
			'user': forms.Select(attrs = 
				{
				'required':'',
				'title':'Seleccione el Usuario.',
				}),
			'aula': forms.Select(attrs = 
				{
				'required':'',
				'title':'Seleccione Aula.',
				}),
			'apoderado': forms.Select(attrs = 
				{
				'required':'',
				'title':'Seleccione Aula.',
				}),
			'dni': forms.NumberInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Ingrese su DNI.',
				}),

			'hobby': forms.TextInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				}),
			'telefono': forms.NumberInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Ingrese su Telefono.',
				'autofocus':''
				}),
			'foto': forms.FileInput(attrs = 
				{
				'class':'form-control',
				'title':'Ingrese su foto',
				'autofocus':''
				}),
		}
class ApoderadoForm(forms.ModelForm):
	class Meta:
		model = Apoderado
		fields = ('user','dni', 'telefono', 'foto')
		widgets = {
			'user': forms.Select(attrs = 
				{
				'required':'',
				'title':'Seleccione el Usuario.',
				}),
			'dni': forms.NumberInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Ingrese su DNI.',
				}),
			'telefono': forms.NumberInput(attrs = 
				{
				'class':'form-control',
				'required':'',
				'title':'Ingrese su Telefono.',
				'autofocus':''
				}),
			'foto': forms.FileInput(attrs = 
				{
				'class':'form-control',
				'title':'Ingrese su foto',
				'autofocus':''
				}),
		}


