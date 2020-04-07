from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.template.defaultfilters import slugify
#from fcm_django.models import FCMDevice


#login
class UserManager(BaseUserManager):
	def _create_user(self, username, email, password, is_active,is_staff, is_superuser, **extra_fields):
		#if not email:
			#raise ValueError('El email debe ser obligatorio')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password,True, False, False, **extra_fields)
	def create_user_email(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password,False, False, False, **extra_fields)
	def create_superuser(self, username, email, password, **extra_fields):
		return self._create_user(username, email, password,True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(max_length=75, unique=False)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	avatar = models.URLField(null=True, blank=True, default="https://s3-us-west-2.amazonaws.com/capuly/static/img/icon-user-default.png")
	
	status = models.BooleanField(default=False)
	objects = UserManager()

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	es_administrador= models.BooleanField(default=False)
	es_profesor = models.BooleanField(default=False)
	es_estudiante = models.BooleanField(default=False)
	es_apoderado= models.BooleanField(default=False)


	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	MASCULINO = 1
	FEMENINO = 2
	GENERO_TYPES = ((MASCULINO, 'Masculino'),(FEMENINO, 'Femenino'),)
	genero = models.PositiveSmallIntegerField(choices=GENERO_TYPES, default=1)

	def get_short_name(self):
		return self.username

	def __unicode__(self): 
		return "%s - %s " % (self.username, self.first_name)

class TimeStampModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	#al momento de crearla no se creara como una tabla
	class Meta:
		abstract =True


class Colegio(TimeStampModel):
	nombre = models.CharField(max_length=100)
	numero = models.IntegerField()
	direccion = models.CharField(max_length=100)
	telefono = models.IntegerField()

	foto = models.ImageField(upload_to='images/colegios/', null=True, blank=True, default=None) 

	slug = models.SlugField(editable=False)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Colegio, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s" % (self.nombre)

class Nivel(TimeStampModel):
	nivel = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(editable=False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nivel)
		super(Nivel, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s" % (self.nivel)

class Grado(TimeStampModel):
	grado = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(editable=False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.grado)
		super(Grado, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s" % (self.grado)

class Seccion(TimeStampModel):
	seccion = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(editable=False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.seccion)
		super(Seccion, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s" % (self.seccion)

class Profesion(TimeStampModel):
	nombre = models.CharField(max_length=100, unique=True)
	descripcion = models.CharField(max_length=200)
	slug = models.SlugField(editable=False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Profesion, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s" % (self.nombre)


class Administrador(TimeStampModel):
	user = models.OneToOneField(User)
	dni = models.IntegerField()
	hobby = models.CharField(max_length=100)
	foto = models.ImageField(upload_to='images/administradores/', null=True, blank=True, default=None)
	telefono = models.IntegerField()
	slug = models.SlugField(editable=False)

	profesion = models.ForeignKey(Profesion)

	colegio_defecto = models.ForeignKey(Colegio)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.user.first_name)
		super(Administrador, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s %s" % (self.user.first_name, self.user.last_name)


class Profesor(TimeStampModel):
	user = models.OneToOneField(User)
	dni = models.IntegerField()
	hobby = models.CharField(max_length=100)
	foto = models.ImageField(upload_to='images/profesores/', null=True, blank=True, default=None)
	telefono = models.IntegerField()
	slug = models.SlugField(editable=False)

	profesion = models.ForeignKey(Profesion)

	colegio_defecto = models.ForeignKey(Colegio)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.user.first_name)
		super(Profesor, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s %s" % (self.user.first_name, self.user.last_name)



class Apoderado(TimeStampModel):
	user = models.OneToOneField(User)
	dni = models.IntegerField()
	telefono = models.IntegerField()
	foto = models.ImageField(upload_to='images/apoderados/', null=True, blank=True, default=None)
	slug = models.SlugField(editable=False)

	#colegio_defecto = models.ForeignKey(Colegio)
	hijo_defecto = models.IntegerField( null=True, blank=True, default=0)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.user.first_name)
		super(Apoderado, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s %s" % (self.user.first_name, self.user.last_name)



class Curso(TimeStampModel):
	nombre = models.CharField(max_length=100, unique=False)
	descripcion = models.CharField(max_length=200)
	colegio = models.ForeignKey(Colegio)
	slug = models.SlugField(editable=False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Curso, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s" % (self.nombre)

class Aula(TimeStampModel):
	#usuario = models.ForeignKey(User)
	colegio = models.ForeignKey(Colegio)
	nivel = models.ForeignKey(Nivel)
	grado = models.ForeignKey(Grado)
	seccion = models.ForeignKey(Seccion)
	#profesor = models.ForeignKey(Profesor)
	def __unicode__(self): 
		return "%s %s %s" % (self.grado, self.seccion, self.nivel)

class DetalleAulaCurso(TimeStampModel):
	aula = models.ForeignKey(Aula)
	curso = models.ForeignKey(Curso)
	def __unicode__(self): 
		return "%s - %s" % (self.aula, self.curso)

class DetalleAulaProfesor(TimeStampModel):
	profesor = models.ForeignKey(Profesor)
	aula = models.ForeignKey(Aula)
	def __unicode__(self): 
		return "%s - %s" % (self.profesor, self.aula)

class DetalleProfesorCurso(TimeStampModel):
	profesor = models.ForeignKey(Profesor)
	curso = models.ForeignKey(DetalleAulaCurso) #new
	def __unicode__(self): 
		return "%s - %s" % (self.profesor, self.curso)

class Estudiante(TimeStampModel):
	user = models.OneToOneField(User)
	aula = models.ForeignKey(Aula)
	apoderado = models.ForeignKey(Apoderado)

	dni = models.IntegerField()
	hobby = models.CharField(max_length=100)
	telefono = models.IntegerField()
	foto = models.ImageField(upload_to='images/estudiantes/', null=True, blank=True, default=None)
	slug = models.SlugField(editable=False)

	colegio_defecto = models.ForeignKey(Colegio)
	
	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.user.first_name)
		super(Estudiante, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s %s" % (self.user.first_name, self.user.last_name)


class Matricula(TimeStampModel):
	estudiante = models.ForeignKey(Estudiante)
	aula = models.ForeignKey(Aula)
	def __unicode__(self): 
		return "%s - %s" % (self.user.estudiante, self.aula)


class Asistencia(TimeStampModel):

	ASISTENCIA = 1
	TARDANZA = 2
	FALTA = 3
	ASISTENCIA_TYPES = ((ASISTENCIA, 'Asistencia'),(TARDANZA, 'Tardanza'),(FALTA, 'Falta'),)

	estudiante = models.ForeignKey(Estudiante)
	curso = models.ForeignKey(Curso)
	aula = models.ForeignKey(Aula)
	estado = models.PositiveSmallIntegerField(choices=ASISTENCIA_TYPES)
	fecha  = models.DateField()

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.estudiante.user.first_name)
		super(Asistencia, self).save(*args, **kwargs)
	def __unicode__(self): 
		return "%s - %s" % (self.estudiante.user.first_name, self.fecha)


class AsistenciaAula(TimeStampModel):
	MANANA = 1
	TARDE = 2
	NOCHE = 3
	TURNO_TYPES = ((MANANA, 'Manana'),(TARDE, 'Tarde'),(NOCHE, 'Noche'),)
	aula = models.ForeignKey(Aula)
	curso = models.ForeignKey(Curso)
	turno = models.PositiveSmallIntegerField(choices=TURNO_TYPES)
	fecha  = models.DateField()
	def __unicode__(self): 
		return "%s - %s" % (self.aula, self.fecha)


class DetalleAdministradorColegio(TimeStampModel):
	administrador = models.ForeignKey(Administrador)
	colegio = models.ForeignKey(Colegio)
	def __unicode__(self): 
		return "%s - %s" % (self.administrador, self.colegio)


class DetalleEstudianteColegio(TimeStampModel):
	estudiante = models.ForeignKey(Estudiante)
	colegio = models.ForeignKey(Colegio)

	def __unicode__(self): 
		return "%s - %s" % (self.estudiante, self.colegio)


class DetalleProfesorColegio(TimeStampModel):
	profesor = models.ForeignKey(Profesor)
	colegio = models.ForeignKey(Colegio)

	def __unicode__(self): 
		return "%s - %s" % (self.profesor, self.colegio)


class DetalleApoderadoColegio(TimeStampModel):
	apoderado = models.ForeignKey(Apoderado)
	colegio = models.ForeignKey(Colegio)

	def __unicode__(self): 
		return "%s" % (self.apoderado)


'''class DetalleAulaColegio(TimeStampModel):
	aula = models.ForeignKey(Aula)
	colegio = models.ForeignKey(Colegio)
	def __unicode__(self): 
		return "%s - %s" % (self.aula, self.colegio)'''


class DetalleApoderadoEstudiante(TimeStampModel):
	apoderado = models.ForeignKey(Apoderado)
	estudiante = models.ForeignKey(Estudiante)

	def __unicode__(self): 
		return "%s - %s" % (self.apoderado, self.estudiante)


class Observacion(TimeStampModel):
	estudiante = models.ForeignKey(Estudiante)
	profesor = models.ForeignKey(Profesor)
	descripcion = models.TextField()
	curso = models.ForeignKey(Curso)
	def __unicode__(self): 
		return "%s - %s" % (self.estudiante.user.first_name, self.descripcion)


class Calificacion(TimeStampModel):
	estudiante = models.ForeignKey(Estudiante)
	profesor = models.ForeignKey(Profesor)
	curso = models.ForeignKey(Curso)
	nota = models.FloatField()
	descripcion = models.TextField(null=True)

	def __unicode__(self): 
		return "%s - %s - %s" % (self.estudiante.user.first_name, self.curso, self.nota)

class Tarea(TimeStampModel):
	profesor = models.ForeignKey(Profesor)
	aula = models.ForeignKey(Aula)
	curso = models.ForeignKey(Curso)
	title = models.CharField(max_length=200)
	detail = models.TextField(null=True)
	start  = models.DateField()
	end  = models.DateField()


	def __unicode__(self): 
		return "%s - %s - %s" % (self.profesor, self.curso, self.title)
