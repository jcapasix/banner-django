#-*- coding: utf-8 -*-
from django import forms
from app.db.models import *

class CalificacionFrom(forms.ModelForm):
	class Meta:
		model = Calificacion
		fields = ('curso', 'nota', 'descripcion',)


class ObservacionFrom(forms.ModelForm):
	class Meta:
		model = Observacion
		fields = ('descripcion',)
