# -*- coding: utf-8 -*-
from __future__ import unicode_literals #

from dataclasses import field

from django.contrib import admin
from appportafolio.models import *
from django.contrib.auth.models import User #
from .models import Mensaje #chat
from .models import Estado, Tarea

#AÑADIR, EDITAR, ELIMINAR, ... DATOS COMO ADMINISTRADOR

admin.site.site_header = "Sitio web Salmantino"  #este es el título
admin.site.site_title = "Portal de Saludos"
admin.site.index_title = "Bienvenidos al portal de Administración"


class HabilidadAdmin(admin.ModelAdmin):
	list_display = [co.name for co in Habilidad._meta.get_fields()]
	search_fields = ('id','habilidad') #siempre tienen que ser una tupla
	list_filter   = ('id','habilidad') #siempre tienen que ser una tupla
admin.site.register(Habilidad, HabilidadAdmin)

class PersonalAdmin(admin.ModelAdmin):
	list_display = [co.name for co in Personal._meta.get_fields()] #lista
	search_fields = ('id','nombre','apellido1','apellido2', 'edad') #tupla
	list_filter   = ('id','nombre') #tupla
admin.site.register(Personal, PersonalAdmin)

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ['id', 'nombre_categoria']
	search_fields = ('id', 'nombre_categoria')
	list_filter = ('id', 'nombre_categoria')
admin.site.register(Categoria, CategoriaAdmin)

#[#lista]
#(#tupla)
#{#diccionario}

class EstudiosAdmin(admin.ModelAdmin):
	#list_display = [co.name for co in Estudio._meta.get_fields()]  # lista
	list_display = [field.name for field in Estudio._meta.fields]  # Solo incluye campos directos del modelo
	search_fields = ('id', 'titulacion', 'fecha_inicio', 'fecha_fin', 'nota_media',
					 "lugarEstudio", "nombreLugar", "ciudad", "presencial", "observaciones")  # tupla
	list_filter = ('id', 'titulacion')
admin.site.register(Estudio, EstudiosAdmin)

#experiencia != ver_experiencia
class ExperienciasAdmin(admin.ModelAdmin):
	list_display = [co.name for co in Experiencia._meta.get_fields()] #lista
	search_fields = ('id','empresa','fecha_inicio','fecha_fin', 'observaciones', 'categoria') #tupla
	list_filter   = ('id','empresa') #esta en models.py
admin.site.register(Experiencia, ExperienciasAdmin)

#29/10/24
class EntrevistadorAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Entrevistador._meta.get_fields() if hasattr(field, 'verbose_name')]
	search_fields = ('id', 'empresa')
admin.site.register(Entrevistador, EntrevistadorAdmin)

#31/10/24
class ImagenAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Imagen._meta.get_fields() if hasattr(field, 'verbose_name')]
	search_fields = ('id', 'imagen')
admin.site.register(Imagen, ImagenAdmin)

class VideoAdmin(admin.ModelAdmin):
	list_display = [field.name for fields in Video._meta.get_fields() if hasattr(field, 'verbose_name')]
	search_fields = ('id', 'video')
admin.site.register(Video, VideoAdmin)

#curriculum 14/11/24
admin.site.register(Curriculum)
#admin.site.register(Estudio)
admin.site.register(DetalleCurriculumEstudio)
admin.site.register(DetalleCurriculumExperiencia)
#admin.site.register(Mensaje)

#18/11/24
class NoticiaAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Noticia._meta.get_fields() if hasattr(field, 'verbose_name')]
	search_fields = ('id', 'titulo')
admin.site.register(Noticia, NoticiaAdmin)

#------------------------------------20-11-24----------------
@admin.register(Valoracion)
class ValoracionAdmin(admin.ModelAdmin):
    list_display = ('id', 'votos_entrevista', 'votos_empresa', 'media_aspectos', 'timestamp')
    readonly_fields = ('media_aspectos',) #,?

    def save_model(self, request, obj, form, change):

        # Calcula automáticamente la media si los votos están presentes
        if obj.votos_entrevista and obj.votos_empresa:
            obj.media_aspectos = (obj.votos_entrevista + obj.votos_empresa) / 2
        super().save_model(request, obj, form, change)

#------------------------------------22-11-24---yo------29-11-24---------------
@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ('remitente', 'destinatario', 'contenido_corto', 'fecha_envio', 'leido')
    list_filter = ('leido', 'fecha_envio')
    search_fields = ('remitente__username', 'destinatario__username', 'contenido')
    ordering = ('-fecha_envio',)
    list_per_page = 20

    def contenido_corto(self, obj):
        return obj.contenido[:50]
    contenido_corto.short_description = 'Contenido'

#------------------------------------------------------------------------------
@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ("id", "estado")

@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    # Muestra el ID, tarea, fecha y nombre del estado
    list_display = ("id", "tarea", "fecha_tarea", "estado_nombre")
    list_filter = ("fkestado", "fecha_tarea")
    search_fields = ("tarea",) #sin la , "coma" es una cadena y no una tupla que es lo que espera python

    # Métdo para mostrar el nombre del estado en lugar del ID
    def estado_nombre(self, obj):
        return obj.fkestado.estado  # Muestra el nombre del estado (ajusta según tu modelo Estado)

    estado_nombre.short_description = "Estado"  # Nombre legible para la columna en el admin

@admin.register(Trabajo)
class TrabajoAdmin(admin.ModelAdmin):
	list_display = ("id", "titulo", "lenguaje", "tecnologias","observaciones", "fecha_proyecto")