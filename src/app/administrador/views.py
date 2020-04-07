#-*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from app.db.models import *
#from django.core.context_processors import csrf
from .forms import *
from django.http import JsonResponse
from django.template.loader import render_to_string

#**************** CURSOS ****************
@login_required(login_url='/')
def curso_list(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        cursos = Curso.objects.filter(colegio__id = administrador.colegio_defecto.id)
        colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        context = {'cursos':cursos, 
        'administrador':administrador, 
        'page_name':'Cursos', 
        'colegios':colegios,
        'colegio':colegio, 
        'curso_active':'active'}
        return render(request, 'administrador/cursos/curso_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_curso_form(request, form, template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        cursos = Curso.objects.filter(colegio__id = administrador.colegio_defecto.id)

        if request.method == 'POST':
            if form.is_valid():
                curso = form.save(commit=False)
                cole = Colegio.objects.get(id=administrador.colegio_defecto.id)
                curso.colegio = cole
                curso.save()

                #Guardamos el Detalla ya que el alumno puede estar en muchos colegios 
                #no guardamoun detalle por que curso pertence a un unico colegio
                #detalle = DetallecursoColegio(curso=curso, colegio=cole)
                #detalle.save()
                data['form_is_valid'] = True
                cursos = Curso.objects.filter(colegio__id = administrador.colegio_defecto.id)
                context = {'cursos': cursos, 'administrador':administrador}
                data['html_curso_list'] = render_to_string('administrador/cursos/partial_curso_list.html', {
                    'cursos': cursos,
                    'administrador':administrador,
                })
            else:
                data['form_is_valid'] = False
            
        context = {'form': form, 'administrador':administrador}

        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')

@login_required(login_url='/')
def curso_create(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        if request.method == 'POST':
            form = CursoForm(request.POST)
        else:
            form = CursoForm()
        return save_curso_form(request, form, 'administrador/cursos/partial_curso_create.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def curso_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        curso = get_object_or_404(Curso, pk=pk)
        if request.method == 'POST':
            form = CursoForm(request.POST, instance=curso)
        else:
            form = CursoForm(instance=curso)
        return save_curso_form(request,form, 'administrador/cursos/partial_curso_update.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def curso_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        curso = get_object_or_404(Curso, pk=pk)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            curso.delete()
            data['form_is_valid'] = True
            cursos = Curso.objects.filter(colegio__id = administrador.colegio_defecto.id)
            data['html_curso_list'] = render_to_string('administrador/cursos/partial_curso_list.html', {
                'cursos': cursos,
                'administrador':administrador,
            })
        else:
            context = {'curso': curso, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/cursos/partial_curso_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')



#**************** AULAS ****************
@login_required(login_url='/')
def aula_list(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
        for aula in aulas:
            aula.profesores = DetalleAulaProfesor.objects.filter(aula__id=aula.id).count()
            aula.cursos =   DetalleAulaCurso.objects.filter(aula__id=aula.id).count()
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        context = {'aulas':aulas, 
        'administrador':administrador, 
        'page_name':'Aulas', 
        'colegio':colegio, 
        'colegios':colegios,
        'aula_active':'active'}

        return render(request, 'administrador/aulas/aula_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_aula_form(request, form, template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
        for aula in aulas:
            aula.profesores = DetalleAulaProfesor.objects.filter(aula__id=aula.id).count()
            aula.cursos =   DetalleAulaCurso.objects.filter(aula__id=aula.id).count()

        if request.method == 'POST':
            if form.is_valid():
                aula = form.save(commit=False)
                cole = Colegio.objects.get(id=administrador.colegio_defecto.id)
                aula.colegio = cole
                aula.save()

                #Guardamos el Detalla ya que el alumno puede estar en muchos colegios 
                #no guardamoun detalle por que aula pertence a un unico colegio
                #detalle = DetalleAulaColegio(aula=aula, colegio=cole)
                #detalle.save()

                data['form_is_valid'] = True
                aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
                for aula in aulas:
                    aula.profesores = DetalleAulaProfesor.objects.filter(aula__id=aula.id).count()
                    aula.cursos =   DetalleAulaCurso.objects.filter(aula__id=aula.id).count()
                context = {'aulas': aulas, 'administrador':administrador}
                data['html_aula_list'] = render_to_string('administrador/aulas/partial_aula_list.html', {
                    'aulas': aulas,
                    'administrador':administrador,
                })
            else:
                data['form_is_valid'] = False
            
        context = {'form': form, 'administrador':administrador}

        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')



@login_required(login_url='/')
def aula_create(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        if request.method == 'POST':
            form = AulaForm(request.POST)
        else:
            form = AulaForm()
        return save_aula_form(request, form, 'administrador/aulas/partial_aula_create.html')
    else:
        return redirect('/')

@login_required(login_url='/')
def aula_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        aula = get_object_or_404(Aula, pk=pk)
        if request.method == 'POST':
            form = AulaForm(request.POST, instance=aula)
        else:
            form = AulaForm(instance=aula)
        return save_aula_form(request,form, 'administrador/aulas/partial_aula_update.html')
    else:
        return redirect('/')

@login_required(login_url='/')
def aula_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        aula = get_object_or_404(Aula, pk=pk)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            aula.delete()
            data['form_is_valid'] = True
            aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
            for aula in aulas:
                aula.profesores = DetalleAulaProfesor.objects.filter(aula__id=aula.id).count()
                aula.cursos =   DetalleAulaCurso.objects.filter(aula__id=aula.id).count()
            data['html_aula_list'] = render_to_string('administrador/aulas/partial_aula_list.html', {
                'aulas': aulas,
                'administrador':administrador,
            })
        else:
            context = {'aula': aula, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/aulas/partial_aula_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')



#**************** PROFESORES ****************
@login_required(login_url='/')
def profesor_list(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        #falta optimizar
        detalle_estudiante = DetalleProfesorColegio.objects.filter(colegio__id = administrador.colegio_defecto.id)
        profesores = getListDetalleProfesores(detalle_estudiante) 
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        context = {
        'profesores':profesores, 
        'administrador':administrador, 
        'page_name':'Profesores', 
        'colegio':colegio,
        'colegios':colegios,  
        'profesor_active':'active'}
        return render(request, 'administrador/profesores/profesor_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_profesor_form(request, formUsuario, formProfesor, opr,template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            if formUsuario.is_valid():
                usuario = formUsuario.save()
                usuario.es_profesor = True
                usuario.set_password(usuario.username)
                usuario.save()

                data['form_is_valid'] = True

                if not usuario == None:
                    if formProfesor.is_valid():
                        profesor = formProfesor.save(commit=False)
                        profesor.user = usuario
                        profesor.dni = usuario.username
                        cole = Colegio.objects.get(id=administrador.colegio_defecto.id)
                        profesor.colegio_defecto = cole
                        profesor.save()
                        if opr == "create":
                            #Guardamos el Detalla ya que el alumno puede estar en muchos colegios 
                            detalle = DetalleProfesorColegio(profesor=profesor, colegio=cole)
                            detalle.save()


                        data['form_is_valid'] = True
                        profesores = Profesor.objects.filter(colegio_defecto__id = administrador.colegio_defecto.id)
                        #context = {'profesores': profesores, 'administrador':administrador}
                        data['html_profesor_list'] = render_to_string('administrador/profesores/partial_profesor_list.html', {
                            'profesores': profesores,
                            'administrador':administrador,
                        })
                else:
                    data['form_is_valid'] = False
            
        context = {'formUsuario': formUsuario, 'formProfesor': formProfesor, 'administrador':administrador}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')


@login_required(login_url='/')
def profesor_create(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        opr = "create"
        if request.method == 'POST':
            formUsuario = UserForm(request.POST)
            formProfesor = ProfesorForm(request.POST)
        else:
            formUsuario = UserForm()
            formProfesor = ProfesorForm()
        return save_profesor_form(request, formUsuario, formProfesor, opr,'administrador/profesores/partial_profesor_create.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def profesor_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        opr = "update"
        profesor = get_object_or_404(Profesor, pk=pk)
        usuario = get_object_or_404(User, pk=profesor.user.id)
        if request.method == 'POST':
            formUsuario = UserForm(request.POST, instance=usuario)
            formProfesor = ProfesorForm(request.POST, instance=profesor)
        else:
            formUsuario = UserForm(instance=usuario)
            formProfesor = ProfesorForm(instance=profesor)
        return save_profesor_form(request, formUsuario, formProfesor, opr,'administrador/profesores/partial_profesor_update.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def profesor_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():   
        profesor = get_object_or_404(Profesor, pk=pk)
        usuario = get_object_or_404(User, pk=profesor.user.id)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            profesor.delete()
            usuario.delete()
            data['form_is_valid'] = True
            profesores = Profesor.objects.filter(colegio_defecto__id = administrador.colegio_defecto.id)
            data['html_profesor_list'] = render_to_string('administrador/profesores/partial_profesor_list.html', {
                'profesores': profesores,
                'administrador':administrador,
            })
        else:
            context = {'profesor': profesor, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/profesores/partial_profesor_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')




#**************** Estudiante ****************
@login_required(login_url='/')
def estudiante_list(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        #falta optimizar
        detalle_estudiante = DetalleEstudianteColegio.objects.filter(colegio__id = administrador.colegio_defecto.id)
        estudiantes = getListDetalleEstudiantes(detalle_estudiante) 
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        context = {
        'estudiantes':estudiantes, 
        'administrador':administrador, 
        'page_name':'Estudiantes', 
        'colegios':colegios,
        'colegio':colegio,  
        'estudiante_active':'active'}
        return render(request, 'administrador/estudiantes/estudiante_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_estudiante_form(request, formUsuario, formEstudiante, opr,template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            if formUsuario.is_valid():
                usuario = formUsuario.save()
                usuario.es_estudiante = True
                usuario.set_password(usuario.username)
                usuario.save()

                data['form_is_valid'] = True

                if not usuario == None:
                    if formEstudiante.is_valid():
                        estudiante = formEstudiante.save(commit=False)
                        estudiante.user = usuario
                        estudiante.dni = usuario.username
                        cole = Colegio.objects.get(id=administrador.colegio_defecto.id)
                        estudiante.colegio_defecto = cole
                        estudiante.save()

                        #Guardamos el Detalla ya que el alumno puede estar en muchos colegios
                        if opr == "create": 
                            detalle_estudiante = DetalleEstudianteColegio(estudiante=estudiante, colegio=cole)
                            detalle_estudiante.save()
                            
                            detalle_apoderado = DetalleApoderadoEstudiante(apoderado=estudiante.apoderado, estudiante=estudiante)
                            detalle_apoderado.save()

                        apoderado = Apoderado.objects.get(id=estudiante.apoderado.id)

                        if apoderado.hijo_defecto == 0:
                            apoderado.hijo_defecto = usuario.username
                            apoderado.save()


                        data['form_is_valid'] = True
                        estudiantes = Estudiante.objects.filter(colegio_defecto__id = administrador.colegio_defecto.id)
                        #context = {'estudiantes': estudiantes, 'administrador':administrador}
                        data['html_estudiante_list'] = render_to_string('administrador/estudiantes/partial_estudiante_list.html', {
                            'estudiantes': estudiantes,
                            'administrador':administrador,
                        })
                else:
                    data['form_is_valid'] = False
            
        context = {'formUsuario': formUsuario, 'formEstudiante': formEstudiante, 'administrador':administrador}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')


@login_required(login_url='/')
def estudiante_create(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        opr = "create"
        if request.method == 'POST':
            formUsuario = UserForm(request.POST)
            formEstudiante = EstudianteForm(request.POST)
        else:
            formUsuario = UserForm()
            formEstudiante = EstudianteForm()
            admin = Administrador.objects.get(user__id=request.user.id)
            formEstudiante.fields['aula'].queryset = Aula.objects.filter(colegio__id=admin.colegio_defecto.id)
            #formEstudiante.fields['apoderado'].queryset = DetalleApoderadoColegio.objects.filter(colegio__id=admin.colegio_defecto.id)
        return save_estudiante_form(request, formUsuario, formEstudiante, opr,'administrador/estudiantes/partial_estudiante_create.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def estudiante_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        opr = "update"
        estudiante = get_object_or_404(Estudiante, pk=pk)
        usuario = get_object_or_404(User, pk=estudiante.user.id)
        if request.method == 'POST':
            formUsuario = UserForm(request.POST, instance=usuario)
            formEstudiante = EstudianteForm(request.POST, instance=estudiante)
        else:
            formUsuario = UserForm(instance=usuario)
            formEstudiante = EstudianteForm(instance=estudiante)
        return save_estudiante_form(request, formUsuario, formEstudiante, opr,'administrador/estudiantes/partial_estudiante_update.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def estudiante_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        estudiante = get_object_or_404(Estudiante, pk=pk)
        usuario = get_object_or_404(User, pk=estudiante.user.id)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            estudiante.delete()
            usuario.delete()
            data['form_is_valid'] = True
            estudiantes = Estudiante.objects.filter(colegio_defecto__id = administrador.colegio_defecto.id)
            data['html_estudiante_list'] = render_to_string('administrador/estudiantes/partial_estudiante_list.html', {
                'estudiantes': estudiantes,
                'administrador':administrador,
            })
        else:
            context = {'estudiante': estudiante, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/estudiantes/partial_estudiante_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')


#**************** Apoderado ****************
@login_required(login_url='/')
def apoderado_list(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        detalle_apoderado = DetalleApoderadoColegio.objects.filter(colegio__id = administrador.colegio_defecto.id)
        apoderados = getListDetalleApoderado(detalle_apoderado) 
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        context = {
        'apoderados':apoderados, 
        'administrador':administrador, 
        'page_name':'Apoderados', 
        'colegio':colegio,
        'colegios':colegios, 
        'apoderado_active':'active'}
        return render(request, 'administrador/apoderados/apoderado_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_apoderado_form(request, formUsuario, formApoderado, opr,template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            if formUsuario.is_valid():
                usuario = formUsuario.save()
                usuario.es_apoderado = True
                usuario.set_password(usuario.username)
                usuario.save()

                data['form_is_valid'] = True

                if not usuario == None:
                    if formApoderado.is_valid():
                        apoderado = formApoderado.save(commit=False)
                        apoderado.user = usuario
                        apoderado.dni = usuario.username
                        cole = Colegio.objects.get(id=administrador.colegio_defecto.id)
                        #apoderado.colegio_defecto = cole
                        apoderado.save()

                        #Guardamos el Detalla ya que el alumno puede estar en muchos colegios 
                        if opr == "create":
                            detalle_apoderado = DetalleApoderadoColegio(apoderado=apoderado, colegio=cole)
                            detalle_apoderado.save()

                        data['form_is_valid'] = True
                        #importante cambiar en todos los modeos estas dos lineas tambienen eliminar
                        detalle_apoderado = DetalleApoderadoColegio.objects.filter(colegio__id = administrador.colegio_defecto.id)
                        apoderados = getListDetalleApoderado(detalle_apoderado) 
                        #apoderados = Apoderado.objects.filter(colegio_defecto__id = administrador.colegio_defecto.id)

                        #context = {'apoderados': apoderados, 'administrador':administrador}
                        data['html_apoderado_list'] = render_to_string('administrador/apoderados/partial_apoderado_list.html', {
                            'apoderados': apoderados,
                            'administrador':administrador,
                        })
                else:
                    data['form_is_valid'] = False
            
        context = {'formUsuario':formUsuario, 'formApoderado':formApoderado, 'administrador':administrador}
        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')



@login_required(login_url='/')
def apoderado_create(request):
    if request.user.es_administrador and not request.user.is_anonymous():
        opr = "create"
        if request.method == 'POST':
            formUsuario = UserForm(request.POST)
            formApoderado = ApoderadoForm(request.POST)
        else:
            formUsuario = UserForm()
            formApoderado = ApoderadoForm()
        return save_apoderado_form(request, formUsuario, formApoderado, opr,'administrador/apoderados/partial_apoderado_create.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def apoderado_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        opr = "update"
        apoderado = get_object_or_404(Apoderado, pk=pk)
        usuario = get_object_or_404(User, pk=apoderado.user.id)
        if request.method == 'POST':
            formUsuario = UserForm(request.POST, instance=usuario)
            formApoderado = ApoderadoForm(request.POST, instance=apoderado)
        else:
            formUsuario = UserForm(instance=usuario)
            formApoderado = ApoderadoForm(instance=apoderado)
        return save_apoderado_form(request, formUsuario, formApoderado, opr,'administrador/apoderados/partial_apoderado_update.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def apoderado_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        apoderado = get_object_or_404(Apoderado, pk=pk)
        usuario = get_object_or_404(User, pk=apoderado.user.id)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            apoderado.delete()
            usuario.delete()
            data['form_is_valid'] = True
            #importante
            #apoderados = Apoderado.objects.filter(colegio_defecto__id = administrador.colegio_defecto.id)
            detalle_apoderado = DetalleApoderadoColegio.objects.filter(colegio__id = administrador.colegio_defecto.id)
            apoderados = getListDetalleApoderado(detalle_apoderado) 
            data['html_apoderado_list'] = render_to_string('administrador/apoderados/partial_apoderado_list.html', {
                'apoderados': apoderados,
                'administrador':administrador,
            })
        else:
            context = {'apoderado': apoderado, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/apoderados/partial_apoderado_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')



#estas funciones permite obtener objetos de un detalle
def getListDetalleEstudiantes(obj):
    nuewObj = list()
    for e in obj:
        nuewObj.append(e.estudiante)
    return nuewObj

def getListDetalleProfesores(obj):
    nuewObj = list()
    for e in obj:
        nuewObj.append(e.profesor)
    return nuewObj


def getListDetalleApoderado(obj):
    nuewObj = list()
    for e in obj:
        nuewObj.append(e.apoderado)
    return nuewObj



#**************** DETALLES ****************

@login_required(login_url='/')
def aula_cursos(request, aula_pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        detalles = DetalleAulaCurso.objects.filter(aula__id=aula_pk)
        #aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
        #colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        page_name = "Cursos asisgnados al Aula"
        context = {
        'detalles':detalles,
        'aula_pk':aula_pk, 
        'colegio':colegio,
        'page_name':page_name,
        'aula_active':'active'}
        return render(request, 'administrador/aulas_cursos/aula_cursos_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_aula_cursos_form(request, aula_pk, form, template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            if form.is_valid():
                detalle = form.save(commit=False)
                detalle.aula = Aula.objects.get(id=aula_pk)
                detalle.save()
                data['form_is_valid'] = True
                detalles = DetalleAulaCurso.objects.filter(aula__id=aula_pk)
                context = {'detalles': detalles, 'administrador':administrador}
                data['html_aula_cursos_list'] = render_to_string('administrador/aulas_cursos/partial_aula_cursos_list.html', {
                    'detalles': detalles,
                    'administrador':administrador,
                })
            else:
                data['form_is_valid'] = False
            
        context = {'form': form, 'aula_pk':aula_pk, 'administrador':administrador}

        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')


@login_required(login_url='/')
def aula_cursos_create(request, aula_pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        if request.method == 'POST':
            form = DetalleAulaCursoForm(request.POST)
        else:
            #new
            form = DetalleAulaCursoForm()
            admin = Administrador.objects.get(user__id=request.user.id)
            form.fields['curso'].queryset = Curso.objects.filter(colegio__id=admin.colegio_defecto.id)
        return save_aula_cursos_form(request, aula_pk, form, 'administrador/aulas_cursos/partial_aula_cursos_create.html')

    else:
        return redirect('/')


@login_required(login_url='/')
def aula_cursos_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalle = get_object_or_404(DetalleAulaCurso, pk=pk)
        aula_pk = detalle.aula.id
        if request.method == 'POST':
            form = DetalleAulaCursoForm(request.POST, instance=detalle)
        else:
            form = DetalleAulaCursoForm(instance=detalle)
        return save_aula_cursos_form(request,aula_pk,form, 'administrador/aulas_cursos/partial_aula_cursos_update.html')

    else:
        return redirect('/')



@login_required(login_url='/')
def aula_cursos_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalle = get_object_or_404(DetalleAulaCurso, pk=pk)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            detalle.delete()
            data['form_is_valid'] = True
            detalles = DetalleAulaCurso.objects.filter(aula__id=detalle.aula.id)
            #detalles = DetalleAulaCurso.objects.filter(colegio__id = administrador.colegio_defecto.id)
            data['html_aula_cursos_list'] = render_to_string('administrador/aulas_cursos/partial_aula_cursos_list.html', {
                'detalles': detalles,
                'administrador':administrador,
            })
        else:
            context = {'detalle': detalle, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/aulas_cursos/partial_aula_cursos_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')


#Aula - profesores
@login_required(login_url='/')
def aula_profesores(request, aula_pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalles = DetalleAulaProfesor.objects.filter(aula__id=aula_pk)
        #aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
        #colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)

        page_name = "Profesores en Aula"
        context = {'detalles':detalles,'aula_pk':aula_pk, 'page_name':page_name,'aula_active':'active'}
        return render(request, 'administrador/aulas_profesores/aula_profesores_list.html', context)
    else:
        return redirect('/')


@login_required(login_url='/')
def save_aula_profesores_form(request, aula_pk, form, template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            if form.is_valid():
                detalle = form.save(commit=False)
                detalle.aula = Aula.objects.get(id=aula_pk)
                detalle.save()
                data['form_is_valid'] = True
                detalles = DetalleAulaProfesor.objects.filter(aula__id=aula_pk)
                context = {'detalles': detalles, 'administrador':administrador}
                data['html_aula_profesores_list'] = render_to_string('administrador/aulas_profesores/partial_aula_profesores_list.html', {
                    'detalles': detalles,
                    'administrador':administrador,
                })
            else:
                data['form_is_valid'] = False
            
        context = {'form': form, 'aula_pk':aula_pk, 'administrador':administrador}

        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')        

@login_required(login_url='/')
def aula_profesores_create(request, aula_pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        if request.method == 'POST':
            form = DetalleAulaProfesorForm(request.POST)
        else:
            form = DetalleAulaProfesorForm()
        return save_aula_profesores_form(request, aula_pk, form, 'administrador/aulas_profesores/partial_aula_profesores_create.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def aula_profesores_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalle = get_object_or_404(DetalleAulaProfesor, pk=pk)
        aula_pk = detalle.aula.id
        if request.method == 'POST':
            form = DetalleAulaProfesorForm(request.POST, instance=detalle)
        else:
            form = DetalleAulaProfesorForm(instance=detalle)
        return save_aula_profesores_form(request,aula_pk,form, 'administrador/aulas_profesores/partial_aula_profesores_update.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def aula_profesores_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalle = get_object_or_404(DetalleAulaProfesor, pk=pk)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            detalle.delete()
            data['form_is_valid'] = True
            detalles = DetalleAulaProfesor.objects.filter(aula__id=detalle.aula.id)
            #detalles = DetalleAulaProfesor.objects.filter(colegio__id = administrador.colegio_defecto.id)
            data['html_aula_profesores_list'] = render_to_string('administrador/aulas_profesores/partial_aula_profesores_list.html', {
                'detalles': detalles,
                'administrador':administrador,
            })
        else:
            context = {'detalle': detalle, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/aulas_profesores/partial_aula_profesores_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')




#Detalle Profesor Cursos
@login_required(login_url='/')
def profesor_cursos(request, profesor_pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        administrador = Administrador.objects.get(user__id = request.user.id)
        detalles = DetalleProfesorCurso.objects.filter(profesor__id=profesor_pk)
        #aulas = Aula.objects.filter(colegio__id = administrador.colegio_defecto.id)
        #colegios = DetalleAdministradorColegio.objects.filter(administrador__user__id=request.user.id)
        colegio = Colegio.objects.get(id = administrador.colegio_defecto.id)
        page_name = "Cursos Asignados al Profesor"
        context = {
        'detalles':detalles, 
        'profesor_pk':profesor_pk, 
        'colegio':colegio,
        'page_name':page_name, 
        'profesor_active':'active'}

        return render(request, 'administrador/profesores_cursos/profesor_cursos_list.html', context)
    else:
        return redirect('/')

@login_required(login_url='/')
def save_profesor_cursos_form(request, profesor_pk, form, template_name):
    if request.user.es_administrador and not request.user.is_anonymous():
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            if form.is_valid():
                detalle = form.save(commit=False)
                detalle.profesor = Profesor.objects.get(id=profesor_pk)
                detalle.save()
                data['form_is_valid'] = True
                detalles = DetalleProfesorCurso.objects.filter(profesor__id=profesor_pk)
                context = {'detalles': detalles, 'administrador':administrador}
                data['html_profesor_cursos_list'] = render_to_string('administrador/profesores_cursos/partial_profesor_cursos_list.html', {
                    'detalles': detalles,
                    'administrador':administrador,
                })
            else:
                data['form_is_valid'] = False
            
        context = {'form': form, 'profesor_pk':profesor_pk, 'administrador':administrador}

        data['html_form'] = render_to_string(template_name, context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')



@login_required(login_url='/')
def profesor_cursos_create(request, profesor_pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        if request.method == 'POST':
            form = DetalleProfesorCursoForm(request.POST)
        else:
            form = DetalleProfesorCursoForm()
            admin = Administrador.objects.get(user__id=request.user.id)
            #optimizar
            #filtrar
            form.fields['curso'].queryset = DetalleAulaCurso.objects.filter(curso__colegio__id=admin.colegio_defecto.id)
            #form.fields["cursos"].queryset = Photo.objects.filter(user=request.user)
        return save_profesor_cursos_form(request, profesor_pk, form, 'administrador/profesores_cursos/partial_profesor_cursos_create.html')

    else:
        return redirect('/')


@login_required(login_url='/')
def profesor_cursos_update(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalle = get_object_or_404(DetalleProfesorCurso, pk=pk)
        profesor_pk = detalle.profesor.id
        if request.method == 'POST':
            form = DetalleProfesorCursoForm(request.POST, instance=detalle)
        else:
            form = DetalleProfesorCursoForm(instance=detalle)
        return save_profesor_cursos_form(request,profesor_pk,form, 'administrador/profesores_cursos/partial_profesor_cursos_update.html')
    else:
        return redirect('/')


@login_required(login_url='/')
def profesor_cursos_delete(request, pk):
    if request.user.es_administrador and not request.user.is_anonymous():
        detalle = get_object_or_404(DetalleProfesorCurso, pk=pk)
        data = dict()
        administrador = Administrador.objects.get(user__id = request.user.id)
        if request.method == 'POST':
            detalle.delete()
            data['form_is_valid'] = True
            detalles = DetalleProfesorCurso.objects.filter(profesor__id=detalle.profesor.id)
            #detalles = DetalleProfesorCurso.objects.filter(colegio__id = administrador.colegio_defecto.id)
            data['html_profesor_cursos_list'] = render_to_string('administrador/profesores_cursos/partial_profesor_cursos_list.html', {
                'detalles': detalles,
                'administrador':administrador,
            })
        else:
            context = {'detalle': detalle, 'administrador':administrador, }
            data['html_form'] = render_to_string('administrador/profesores_cursos/partial_profesor_cursos_delete.html', context, request=request)
        return JsonResponse(data)
    else:
        return redirect('/')

        
