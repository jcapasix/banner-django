#CALIFICACIONES 
def calificaciones_index(request):
	if request.user.is_anonymous():
		return redirect('/')
	if request.user.es_profesor:

		profesor = Profesor.objects.get(user__id = request.user.id)
		#aulas = Aula.objects.filter(colegio__id = profesor.colegio_defecto.id, profesor__id = profesor.id)
		detalles = DetalleProfesorCurso.objects.filter(profesor=profesor)
		colegios = DetalleProfesorColegio.objects.filter(profesor__user__id=request.user.id)
		context = {'detalles':detalles, 'profesor':profesor, 'page_name':'Calificaciones', 'colegios':colegios, 'calificaciones_active':'active'}
		return render(request, 'profesor/calificaciones/calificaciones.html', context)
	else:
		return redirect('/')