# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from django.contrib.auth.models import User #para el user

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
	
class Personal(models.Model): #herencia
	id = models.AutoField(primary_key=True)
	nombre = models.CharField("Nombre", max_length=25, null=True, blank=True)
	apellido1 = models.CharField("Primer apellido", max_length=25, null=True, blank=True)
	apellido2 = models.CharField("Segundo apellido", max_length=25, null=True, blank=True)
	edad = models.IntegerField("Edad", null=True, blank=True)
	usuario = models.ForeignKey(User, related_name='datos_usuario', null=True, blank=True, on_delete=models.PROTECT)

	class Meta:
		verbose_name="Personal"
		verbose_name_plural="Personales"
		ordering = ['nombre'] #orden por defecto
	
	def __str__ (self): #str para concatenar
		return '%s, %s, %s, %s' % (self.nombre, self.apellido1, self.apellido2, self.edad)

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

