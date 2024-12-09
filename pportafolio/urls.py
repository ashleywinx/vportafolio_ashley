# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tkinter.font import names

from django.contrib import admin
from django.urls import path, include, re_path
from appportafolio import views
from appportafolio.views import *

#servicio de ficheros estáticos durante el desarrollo
from django.conf import settings
from django.conf.urls.static import static

#29/10/24
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

#servicio de ficheros estáticos durante el servidor
from django.views.static import serve
#from django.views.static import save
#from pportafolio.settings import MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^$', views.home, name='home'),
    #re_path('', views.home,name='home'),
    path('sobremi/', views.sobremi, name='sobremi'),
    re_path('habilidades/', views.habilidades, name='habilidades'),
    re_path(r'^(?P<id>\d+)/ver_habilidad$', views.ver_habilidad, name='ver_habilidad'),
    path('eliminar_habilidad/<int:eh>/', views.eliminar_habilidad, name='eliminar_habilidad'),
    path('editar_habilidad/<int:mh>/', views.editar_habilidad, name='editar_habilidad'),
    path('crear_habilidad/', views.crear_habilidad, name='crear_habilidad'),#NO NECESITA ID
    re_path('categorias/', views.categorias, name='categorias'),
    re_path('estudios/', views.estudios, name='estudios'),
    re_path('experiencias', views.experiencias, name='experiencias'),
    re_path(r'^(?P<id>\d+)/ver_experiencia$', views.ver_experiencia, name='ver_experiencia'),
    path('eliminar_experiencia/<int:pk>/', views.eliminar_experiencia, name='eliminar_experiencia'),
    re_path('login/', views.login_view, name='login'),
    re_path('register/', register_view, name='register'),
    re_path('cerrar/', views.cerrar, name='cerrar'),

    #path('login/', login_view, name='login'),
    #path('register/', register_view, name='register'),
    path('generar_pdf/<int:entrevistador_id>/', views.generar_pdf, name='generar_pdf'),
    path('listar_entrevistadores/', views.listar_entrevistadores, name='listar_entrevistadores'),

    path('subir_imagenes/', subir_imagenes, name='subir_imagenes'),
    path('imagen/editar/<int:imagen_id>/', views.editar_imagen, name='editar_imagen'),
    path('imagen/eliminar/<int:imagen_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    path('subir_videos/', subir_videos, name='subir_videos'),
    path('video/editar/<int:video_id>/', views.editar_video, name='editar_video'),
    path('video/eliminar/<int:video_id>/', views.eliminar_video, name='eliminar_video'),

    path('contacto/', views.contacto, name='contacto'),
    path('agegar/', views.agregar_curriculum, name='agregar_curriculum'),
    path('ver/<int:pk>/', views.ver_curriculum, name='ver_curriculum'),
    path('generar_pdf/<int:entrevistador_id>/', views.generar_pdf, name='generar_pdf'),

    path('lista_noticias/', views.lista_noticias, name='lista_noticias'),
    path('crear_noticia/', views.crear_noticia, name='crear_noticia'),
    path('listar_valoraciones/', views.listar_valoraciones, name='listar_valoraciones'),
    path('actualizar_valoracion/<int:pk>/edit/', views.actualizar_valoracion, name='actualizar_valoracion'),
    path('añadir_valoración/add/', añadir_valoracion, name='añadir_valoracion'),

    path('chat_view/<int:entrevistador_id>/', views.chat_view, name='chat_view'),
    path('chat/enviar/', views.enviar_mensaje, name='enviar_mensaje'),
    path('seleccionar_entrevistadores/', views.seleccionar_entrevistadores, name='seleccionar_entrevistadores'), #importante

    path('crear_noticia1/', views.crear_noticia1, name='crear_noticia1'),
    #path('actualizar_evento/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'),

    path('listar_calificaciones/',views.listar_calificaciones, name='listar_calificaciones'),
    path('añadir_calificaciones/',views.añadir_calificacion, name='añadir_calificaciones'),

    path('tareas/', views.lista_tareas, name='lista_tareas'),
    path('tareas/crear/', views.crear_tarea, name='crear_tarea'),
    path('tareas/actualizar/<int:evento_id>/', views.actualizar_evento, name='actualizar_evento'),

    path('trabajo/listar/', views.lista_proyectos,name='lista_proyectos'),
    #path('trabajo/crear/<int:proyecto_id>/', views.crear_proyecto, name='crear_ptoyecto'),
    path('trabajo/crear/', views.crear_proyecto, name='crear_proyecto'),
    re_path('empresa/', views.empresa, name='empresa'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve,{
        'document_root': settings.MEDIA_ROOT,
    })
]