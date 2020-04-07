from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

from app.db.models import *

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class AsistenciasSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.nombre')
    nombre = serializers.ReadOnlyField(source='estudiante.user.first_name')
    apellidos = serializers.ReadOnlyField(source='estudiante.user.last_name')
    class Meta:
        model = Asistencia
        fields = ('id', 'estudiante','nombre','apellidos', 'curso', 'aula', 'estado', 'fecha', 'created')


class CalificacionesSerializer(serializers.ModelSerializer):
    
    curso = serializers.ReadOnlyField(source='curso.nombre')
    class Meta:
        model = Calificacion
        fields = ('id', 'estudiante', 'profesor', 'curso', 'nota', 'descripcion', 'created')


class ObservacionesSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.nombre')
    class Meta:
        model = Observacion
        fields = ('id', 'estudiante', 'profesor', 'curso', 'descripcion', 'created')


class ProfesorSerializer(serializers.ModelSerializer):
    nombre = serializers.ReadOnlyField(source='user.first_name')
    apellidos = serializers.ReadOnlyField(source='user.last_name')
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = Profesor
        fields = ('id', 'user', 'nombre', 'apellidos')


class TareasSerializer(serializers.ModelSerializer):
    #start = serializers.ReadOnlyField(source='start')
    curso = serializers.ReadOnlyField(source='curso.nombre')
    profesor_nombres = serializers.ReadOnlyField(source='profesor.user.first_name')
    profesor_apellidos = serializers.ReadOnlyField(source='profesor.user.last_name')
    class Meta:
        model = Tarea
        fields = ('id', 'profesor', 'profesor_nombres', 'profesor_apellidos', 'aula', 'curso', 'title', 'detail','start','end')

class DetalleAulaCursoSerializer(serializers.ModelSerializer):
    nivel = serializers.ReadOnlyField(source='aula.nivel.nivel')
    grado = serializers.ReadOnlyField(source='aula.grado.grado')
    seccion = serializers.ReadOnlyField(source='aula.seccion.seccion')

    colegio = serializers.ReadOnlyField(source='aula.colegio.nombre')
    curso = serializers.ReadOnlyField(source='curso.nombre')
    class Meta:
        model = DetalleAulaCurso
        fields = ('id', 'aula','nivel', 'grado', 'seccion', 'curso', 'colegio')


class DetalleApoderadoEstudianteSerializer(serializers.ModelSerializer):
    estudiante = serializers.ReadOnlyField(source='estudiante.user.username')
    apoderado = serializers.ReadOnlyField(source='apoderado.user.username')

    estudiante_name = serializers.ReadOnlyField(source='estudiante.user.first_name')
    estudiante_genero = serializers.ReadOnlyField(source='estudiante.user.genero')
    class Meta:
        model = DetalleApoderadoEstudiante
        fields = ('id', 'estudiante','apoderado', 'estudiante_name', 'estudiante_genero')


from . import constants
from rest_framework import generics, permissions, status, response, views
from django.contrib.auth import authenticate, get_user_model

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=False, style={'input_type': 'password'})

    default_error_messages = {
        'inactive_account': constants.INACTIVE_ACCOUNT_ERROR,
        'invalid_credentials': constants.INVALID_CREDENTIALS_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields[User.USERNAME_FIELD] = serializers.CharField(required=False)

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get(User.USERNAME_FIELD), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])



from rest_framework.authtoken.models import Token

class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = (
            'auth_token',
        )
