# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User #para el user
from django.utils import timezone
from .models import *

from django import forms

#LOS MODELOS SON LAS TABLAS DE LA BASE DE DATOS :)

################################################
# Tabla 1 - Habilidades 
################################################
class Habilidad(models.Model):  
	id = models.AutoField(primary_key=True)
	habilidad = models.CharField("Habilidad",max_length=25, null=True, blank=True)
	nivel= models.IntegerField("Nivel", null=True, blank=True) # 1 al 10
	
	class Meta:
		verbose_name = "Habilidad"  #puede ser otro nombre
		verbose_name_plural = "Habilidades"
		ordering = ['habilidad']
	
	def __str__(self):
		return '%s,%s' % (self.habilidad, self.nivel)

################################################
# Personal
################################################
class Personal(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField("Nombre", max_length=25, null=True, blank=True)
	apellido1 = models.CharField("Primer apellido", max_length=25, null=True, blank=True)
	apellido2 = models.CharField("Segundo apellido", max_length=25, null=True, blank=True)
	edad = models.IntegerField("Edad", null=True, blank=True)
	usuario = models.ForeignKey(User, related_name='datos_usuario', null=True, blank=True, on_delete=models.PROTECT)

	class Meta:
		verbose_name = "Personal"
		verbose_name_plural = "Personales"
		ordering = ['nombre']

	def __str__(self):
		return f'{self.nombre}, {self.apellido1}, {self.apellido2}, {self.edad}'

################################################
# Categoria
################################################
class Categoria(models.Model):
	id = models.AutoField(primary_key=True)
	nombre_categoria = models.CharField("Nombre", max_length=25, null=True, blank=True)

	class Meta:
		verbose_name = "Categoria"
		verbose_name_plural="Categorias"
		ordering = ['nombre_categoria'] #esto ira a admin.py

	def __str__(self):
		return '%s, %s' % (self.id, self.nombre_categoria)

##################################
# ESTUDIOS                       #
##################################
class Estudio(models.Model):
	id = models.AutoField(primary_key=True)
	titulacion = models.TextField("Titulo", null=True, blank=True)
	fecha_inicio = models.DateField("Fecha Inicio", null=True, blank=True)
	fecha_fin = models.DateField("Fecha Fin", null=True, blank=True)
	nota_media = models.DecimalField("Nota Media", decimal_places=2, max_digits=4, null=True, blank=True)
	lugarEstudio = models.TextField("Lugar Estudio", null=True, blank=True)
	nombreLugar = models.TextField("Nombre Lugar", null=True, blank=True)
	ciudad = models.CharField("Ciudad", max_length=25, null=True, blank=True)
	presencial = models.BooleanField("Presencial", default=False)
	observaciones = models.TextField("Observaciones", null=True, blank=True)

	class Meta:
		verbose_name = "Estudio"  #puede ser otro nombre
		verbose_name_plural = "Estudios"
		ordering = ['titulacion']

	def __str__(self):
		return '%s, %s, %s, %s, %s, %s, %s, %s, %s' % (self.id, self.titulacion, self.fecha_inicio,self.fecha_fin, self.nota_media,
						   self.lugarEstudio, self.ciudad, self.presencial, self.observaciones)

################################################
# 2 - Experiencia != ver_experiencia
################################################
class Experiencia(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField('Empresa',max_length=50,null=True, blank=True)
    fecha_inicio= models.DateField('Fecha de Inicio',null=True, blank=True)
    fecha_fin = models.DateField('Fecha de Finalización', null=True, blank=True)
    observaciones = models.CharField('Funciones', max_length=50, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, related_name='expe_categoria', null=True, blank=True, on_delete=models.PROTECT)
	#categoria = models.CharField('Categoria', max_length=25, null=True, blank=True)

    class Meta:
        verbose_name = 'Experiencia' #puede ser otro nombre
        verbose_name_plural = 'Experiencias'
        ordering = ['empresa'] #admin.py

    def __str__(self):
        return "%s,%s,%s,%s,%s,%s % (self.id,self.empresa.self.fecha_inicio,self.fecha_fin,self.observaciones,self.categoria)"

#######################
# Los Entrevistadores # 29/10/2024
#######################
class Entrevistador(models.Model):
	id = models.AutoField(primary_key=True)
	avatar = models.ImageField('Avatar', blank=True, null=True, upload_to="media/")
	empresa = models.CharField('Empresa', max_length=30, null=True, blank=True)
	fecha_entrevista = models.DateField('Fecha Entrevista', null=True, blank=True)
	conectado = models.BooleanField('Conectado', null=True, blank=True)
	seleccionado = models.BooleanField('Seleccionado', null=True, blank=True)

	#forteigns keys requerido desde django 2.0
	user = models.ForeignKey(User, related_name='entrevistados_usuario', null=True, blank=True, on_delete=models.PROTECT)

	class Meta:
		verbose_name = 'Entrevistador'
		verbose_name_plural = 'Entrevistadores'
		ordering = ['empresa']

	def __str__(self):
		return "%s, %s, %s, %s, %s, %s" % (self.id, self.empresa, self.fecha_entrevista, self.conectado, self.seleccionado, self.user)

#######################
# IMÁGENES # 31/10/24 #
#######################
class Imagen(models.Model):
	id = models.AutoField(primary_key=True)
	imagen = models.ImageField("Imagen", blank=True, null=True, upload_to="imagenes/")
	comentario = models.CharField('Comentario', max_length=100, null=True, blank=True)

	class Meta:
		verbose_name = 'Imagen'
		verbose_name_plural = 'Imagenes'
		ordering = ['id']

	def __str__(self):
		return "%s, %s, %s" % (self.id, self.imagen, self.comentario)

#####################
# VIDEOS # 31/10/24 #
#####################
class Video(models.Model):
	id = models.AutoField(primary_key=True)
	video = models.FileField("Video", blank=True, null=True, upload_to="videos/")
	comentario = models.CharField('Comentario', max_length=100, null=True, blank=True)

	class Meta:
		verbose_name = 'video'
		verbose_name_plural = 'videos'
		ordering = ['id']

	def __str__(self):
		return "%s, %s, %s" % (self.id, self.video, self.comentario)

################################################
# CURRICULUM - 8/11/24 - YO - 14/11/24
################################################
class Curriculum(models.Model):
    id = models.AutoField(primary_key=True)
    personal = models.ForeignKey('Personal', on_delete=models.CASCADE, related_name='curriculums')
    email = models.EmailField("Email", max_length=100, null=True, blank=True)
    telefono = models.IntegerField("Telefono", null=True, blank=True)

    class Meta:
        verbose_name = 'curriculum'
        verbose_name_plural = 'curriculums'
        ordering = ['id']

    def __str__(self):
        return f"Curriculum de {self.personal.nombre} {self.personal.apellido1} {self.personal.apellido2}"

# Modelo DetalleCurriculumEstudio
class DetalleCurriculumEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    estudio = models.ForeignKey(Estudio, on_delete=models.CASCADE, related_name='detalle_curriculums')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)

    def __str__(self):
        return f"Estudio: {self.estudio.titulacion} para el curriculum de {self.curriculum.personal.nombre}"


# Modelo DetalleCurriculumExperiencia
class DetalleCurriculumExperiencia(models.Model):
    id = models.AutoField(primary_key=True)
    experiencia = models.ForeignKey(Experiencia, on_delete=models.CASCADE)
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE)

    def __str__(self):
        return f"Experiencia: {self.experiencia.empresa} para el curriculum de {self.curriculum.personal.nombre}"

################################################
# NOTICIAS 18/11/24
################################################
class Noticia(models.Model):
	id = models.AutoField(primary_key=True)
	titulo = models.CharField("Titulo", max_length=200, null=True, blank=True)
	contenido = models.TextField()
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	imagen = models.ImageField('Image', blank=True, null=True, upload_to="media/")

	def __str__(self):
		return self.titulo

################################################
# VALORACIÓN - ESTRELLAS - 20/11/24
################################################
class Valoracion (models.Model):
	id = models.AutoField(primary_key = True)
	votos_entrevista = models.DecimalField("Votos Entrevista", max_digits=3, decimal_places=1, null=True, blank=True)
	votos_empresa = models.DecimalField("Votos Empresa", max_digits=3, decimal_places=1, null=True, blank=True)
	media_aspectos = models.DecimalField("Media Aapectos", max_digits=3, decimal_places=1, null=True , blank=True)
	entrevista = models.CharField("Descripción Entrevista", max_length=200, null=True, blank=True)
	empresa = models.CharField("Descripción Empresa", max_length=200, null=True, blank=True)
	num_valoraciones = models.IntegerField("Número de Valoraciones", null=True, blank=True)
	timestamp = models.DateTimeField("Fecha", default=timezone.now)

	def __str__(self):
		return f"{self.id}, {self.votos_entrevista}, {self.votos_empresa}, {self.media_aspectos}, {self.entrevista}, {self.timestamp}"

################################################
# CHAT - 22/11/24
################################################
class Mensaje(models.Model):
	remitente = models.ForeignKey(User, related_name='mensajes_enviados', on_delete=models.CASCADE)
	destinatario =  models.ForeignKey(User, related_name='mensajes_recibidos', on_delete=models.CASCADE)
	contenido = models.TextField('Contenido del mensaje')
	fecha_envio = models.DateTimeField('Fecha de envio', auto_now_add=True)
	leido = models.BooleanField('Leido', default=False)

	class Meta:
		ordering = ['fecha_envio']

	def __str__(self):
		return f"De: {self.remitente.username} Para: {self.destinatario.username} - {self.contenido[:30]}"

#########################
# calificaciones
#########################
class Calificacion(models.Model):
    id = models.AutoField(primary_key=True)
    asignatura = models.CharField("Asignatura", max_length=200, null = True, blank = True)
    nota = models.DecimalField("Nota", max_digits=3, decimal_places=1, null = True, blank = True)

    class Meta:
        verbose_name = "Calificacion"
        verbose_name_plural = "Calificaciones"
        ordering = ['id']

    def __str__(self):
        return f"{self.asignatura},{self.nota}"

################################################
# ESTADO Y TAREAS
################################################
class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=100, verbose_name="Estado")

    def __str__(self):
        return self.estado  # Representación en texto del estado

#-----------------------------------------------
class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    tarea = models.CharField("Anotar Tarea", max_length=200, null=True, blank=True)
    fecha_tarea = models.DateTimeField('Fecha de envio', default=timezone.now) #guarda fecha local y deja actualizar en el form
    fkestado = models.ForeignKey(Estado, on_delete=models.CASCADE, related_name="tareas", verbose_name="Estado asociado")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ['fecha_tarea']  # Orden por defecto

    def __str__(self):
        return self.tarea or f"Tarea sin descripción (ID: {self.id})"

# EXAMEN-----------------------------------------------
class Trabajo(models.Model):
	id = models.AutoField(primary_key=True)
	titulo = models.CharField("nombre proyecto", max_length=200, null=True, blank=True)
	lenguaje = models.CharField(max_length=100, verbose_name="Estado")
	tecnologias = models.CharField(max_length=100, verbose_name="Estado")
	observaciones = models.TextField("Observaciones", null=True, blank=True)
	fecha_proyecto = models.DateField('Fecha de envio', auto_now_add=True)

	class Meta:
		verbose_name = "Trabajo"
		verbose_name_plural = "Trabajos"
		ordering = ["fecha_proyecto"]

	def __str__(self):
		return f"{self.id}, {self.titulo}, {self.lenguaje}, {self.tecnologias}, {self.observaciones}, {self.fecha_proyecto}"
