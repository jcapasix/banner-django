from django.contrib import admin


from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Administrador)
admin.site.register(Profesor)
admin.site.register(Apoderado)
admin.site.register(Estudiante)
admin.site.register(Nivel)
admin.site.register(Aula)
admin.site.register(Curso)

admin.site.register(Profesion)
admin.site.register(Grado)
admin.site.register(Seccion)
admin.site.register(Colegio)
admin.site.register(Asistencia)
admin.site.register(Calificacion)
admin.site.register(Observacion)
admin.site.register(Tarea)
admin.site.register(AsistenciaAula)


admin.site.register(DetalleAdministradorColegio)
admin.site.register(DetalleEstudianteColegio)
admin.site.register(DetalleProfesorColegio)
admin.site.register(DetalleApoderadoColegio)
admin.site.register(DetalleApoderadoEstudiante)


#Matricula
admin.site.register(Matricula)
admin.site.register(DetalleAulaCurso)
admin.site.register(DetalleProfesorCurso)