from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.core import serializers


from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from app.db.models import *

class CalificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calificacion
        fields = ('id', 'estudiante', 'profesor','curso', 'nota', 'descripcion')


class EstudianteSerializer(serializers.ModelSerializer):
    calificacion = CalificacionSerializer()
    class Meta:
        model = Estudiante
        fields = ('id', 'calificacion')