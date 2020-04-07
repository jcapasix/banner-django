from django.shortcuts import render


from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from app.db.models import *
from .serializers import *


class ActionViewMixin(object):
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self._action(serializer)

from rest_framework import response, status, authtoken
from django.contrib.auth import user_logged_in, user_logged_out
def login_user(request, user):
    token, _ = authtoken.models.Token.objects.get_or_create(user=user)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token


def getPerfil(user):
    # administrador 1, profesor 2, estudiante 3, apoderado 4
    if user.es_administrador:
        return 1
    if user.es_profesor:
        return 2
    if user.es_estudiante:
        return 3
    if user.es_apoderado:
        return 4

def getHijo(user):
    if user.es_apoderado:
        apoderado = Apoderado.objects.get(user=user)
        return str(apoderado.hijo_defecto)
    else:
        return None 
def getAutorized(user):
    if user.es_apoderado:
        return True
    else:
        return False 

def getHijoName(user):
    apoderado = Apoderado.objects.get(user=user)
    estudiante = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
    return estudiante.user.first_name+" "+ estudiante.user.last_name

def getHijoEmail(user):
    apoderado = Apoderado.objects.get(user=user)
    estudiante = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
    return estudiante.user.email

def getHijoGenero(user):
    apoderado = Apoderado.objects.get(user=user)
    estudiante = Estudiante.objects.get(user__username=apoderado.hijo_defecto)
    return estudiante.user.genero


class LoginView(ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to obtain user authentication token.
    """
    serializer_class = LoginSerializer
    permission_classes = (
        permissions.AllowAny,
    )

    def _action(self, serializer):
        token = login_user(self.request, serializer.user)
        #token_serializer_class = serializers.serializers_manager.get('token')

        if getAutorized(serializer.user):
            content = {
            'token':token.key,
            'username': serializer.user.username,
            'perfil': getPerfil(serializer.user),
            'hijo': getHijo(serializer.user),
            'hijo_name': getHijoName(serializer.user),
            'hijo_email': getHijoEmail(serializer.user),
            'hijo_genero': getHijoGenero(serializer.user),
            'autorized':getAutorized(serializer.user)}
        else:
            content = {
            'token':token.key,
            'username': serializer.user.username,
            'perfil': getPerfil(serializer.user),
            'autorized':getAutorized(serializer.user)}



        return Response(
            data=content,
            status=status.HTTP_200_OK,
        )




class AsistenciaList(APIView):
    """
    List all asistencias, or create a new snippet.
    """
    def get(self, request, format=None):
        username = request.GET["username"]
        fecha = request.GET["fecha"]
        asistencias = Asistencia.objects.filter(estudiante__user__username=username, fecha=fecha)
        serializer = AsistenciasSerializer(asistencias, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AsistenciasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SonList(APIView):
    """
    List all asistencias, or create a new snippet.
    """
    def get(self, request, format=None):
        username = request.GET["username"]
        detalle = DetalleApoderadoEstudiante.objects.filter(apoderado__user__username=username)
        serializer = DetalleApoderadoEstudianteSerializer(detalle, many=True)
        return Response(serializer.data)



class ChangeSon(APIView):
    def post(self, request, format=None):
        estudiante_username = request.POST.get('estudiante')
        apoderado_username = request.POST.get('apoderado')
        try:
            apoderado = Apoderado.objects.get(user__username = apoderado_username)
            apoderado.hijo_defecto = estudiante_username
            apoderado.save()
            content = {'rpt':True,
                        'estudiante':estudiante_username,
                        'apoderado':apoderado_username}

            return Response(data=content, status=status.HTTP_201_CREATED)
        except Apoderado.DoesNotExist:
            content = {'rpt':False}
            return Response(data=content, status=status.HTTP_400_BAD_REQUEST)


class CalificacionList(APIView):
    """
    List all calificaciones, or create a new snippet.
    """
    def get(self, request, format=None):
        username = request.GET["username"]
        detalle_id = request.GET["detalle"]
        detalle = DetalleAulaCurso.objects.get(id=detalle_id)
        estudiante = Estudiante.objects.get(user__username=username)
        calificaciones = Calificacion.objects.filter(estudiante__user__username=username, curso__id=detalle.curso.id)
        serializer = CalificacionesSerializer(calificaciones, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CalificacionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObservacionList(APIView):
    """
    List all observaciones, or create a new snippet.
    """
    def get(self, request, format=None):
        username = request.GET["username"]
        observaciones = Observacion.objects.filter(estudiante__user__username=username)
        serializer = ObservacionesSerializer(observaciones, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ObservacionesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from datetime import date
class TareaList(APIView):
    """
    List all asistencias, or create a new snippet.
    """
    def get(self, request, format=None):
        username = request.GET["username"]
        fecha = request.GET["fecha"]
        estudiante = Estudiante.objects.get(user__username=username)
        tareas = Tarea.objects.filter(aula__id=estudiante.aula.id, end=fecha)
        serializer = TareasSerializer(tareas, many=True)
        print serializer.data
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TareasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetalleAulaCursoList(APIView):
    """
    List all asistencias, or create a new snippet.
    """
    def get(self, request, format=None):
        username = request.GET["username"]
        estudiante = Estudiante.objects.get(user__username=username)

        detalle = DetalleAulaCurso.objects.filter(aula__id=estudiante.aula.id)
        serializer = DetalleAulaCursoSerializer(detalle, many=True)
        return Response(serializer.data)