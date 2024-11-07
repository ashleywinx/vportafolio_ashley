# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect, get_object_or_404 #
from django.http import HttpResponse
from appportafolio.models import *

from django.shortcuts import redirect #importante tenerlo

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger #paginación
from django.contrib.auth import authenticate, get_user_model, login, logout #todas son por defecto
from django.contrib.auth.decorators import login_required #
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout #
from django.views.decorators.csrf import csrf_protect #

from django.contrib.auth.models import User #
from django.conf import settings #
from django.views.decorators.csrf import csrf_exempt #06/11/24

#email 06/11/24
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages

#------------------------------------------------------------------------------------------------
# Create your views here.
from datetime import datetime
from django.utils import timezone

from django.contrib.auth.models import User

import urllib

#------------------------------------------------------------------------------------------------

def home(request):
    global DEBUG
    print("\033[35mHola estoy en home\033[0m")
    nombreProyecto = 'PORTAFOLIO'
    fechaCreacion = '23/09/2024'
    
    #global FECHA_ARRANQUE
    actual = request.user  # usuario actual
    idusuario = ""
    idusuario = actual.id
    request.session['idusuario'] = idusuario
    numconectados = 0
    dato = ""

    # ip externa o pública
    lista = "0123456789."
    ip = ""

    # ip externa o pública
    lista = "0123456789."
    ip = ""

    '''
    #dato = urllib.urlopen("http://checkip.dyndns.org").read()  # ojo hasta 28/7/2021 usada siempre da error
    #dato = urllib.urlopen("https://free-proxy-list.net").read()  # esta no vacía
    #dato = urllib.urlopen("http://whatismyip.org").read()
    #dato = urllib.urlopen("https://api.ipify.org").read()
    #dato = urllib.urlopen("https://ident.me").read().decode('utf8')  # python 3 este es el guay 28/7/2021
    #https://checkip.amazonaws.com
    '''

    try:
        dato = urllib.request.urlopen('https://www.wikipedia.org').headers['X-Client-IP']  # 7/9/2024 va muy bien
        #dato = urllib.request.urlopen('https://ident.me').read().decode('utf8')  # python 3 este es bueno desde 28/7/2021
        #dato = urllib.urlopen("https://ident.me").read().decode('utf8')  # python 3 este es el bueno 28/7/2021
        print("IP PUBLICA: " + str(dato))
    except:
        print("Error en la Librería de la IP")
        #dato = urllib.urlopen("https://ident.me").read()
        #dato = urllib.request.urlopen('https://ident.me').read() #python 3 el guay 28/7/2021
        #dato = urllib.urlopen("http://checkip.dynds.org").read() #ojo hasta 28/7/2021 usada siempre da error
        dato=""
    finally:
        print ("USUARIO ACTUAL.....["+str(actual)+"]")
    
    for x in str(dato):
        if x in lista:
            ip += x
            
    if str(actual)=="AnonymousUser":
        request.session['tipousuario']='anonimo'
        print("IP ANONIMO....."+str(ip))
        
        #guardamos el evento de la ip del usuario anonimo
        '''
        anonimo=Anonimo()
        anonimo.fecha=timezone.now()
        anonimo.entra=timezone.now()
        anonimo.ip=ip
        anonimo.save()
        '''
    usuario='prueba'
    context={'usuario':usuario, 'nombreProyecto':nombreProyecto, 'fechaCreacion':fechaCreacion}
    return render(request, 'home.html', context=context)

#------------------------------------------------------------------------------------------------

def sobremi(request):
    DEBUG="SI"
    print("\033[35mHola estoy en sobre mi "+str(DEBUG)+"\033[0m")
    nombre = 'ashley'
    edad = 20
    telefono = '654987123'
    cargo = 'peon caminero'
   
    #select*from categoria
    ListaCategorias=Categoria.objects.all().order_by('nombre_categoria')
    
    #es un objetode tipo queryset
    for r in ListaCategorias:
        print(str(r.nombre_categoria))
    context = {'nombre':nombre, 'edad':edad, 'telefono':telefono, 'cargo':cargo, 'ListaCategorias': ListaCategorias}
    return render(request, 'sobremi.html', context=context)

#------------------------------------------------------------------------------------------------

#profe 17/10/2024
def login_view(request):
    print("\033[35mlogin_view\033[0m")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            actual=request.user #usuario actual
            idusuario=0
            idusuario=actual.id
            request.session['idusuario']=idusuario
            print("idusuario="+str(idusuario))
            entrevistador=Entrevistador.objects.get(user=idusuario)
            idEntrevistador=entrevistador.id
            print("idEntrevistador="+str(idEntrevistador))
            print("FOTO="+str(entrevistador.avatar))
            fotoperfil=settings.MEDIA_URL+str(entrevistador.avatar) if entrevistador.avatar else settings.MEDIA_URL+"MONEDA3.jpg"
            print("avatar="+str(fotoperfil))
            context={'fotoperfil': fotoperfil}
            return render(request, 'home.html', context=context)
            #return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Credenciales invalidas'})
    return render(request, 'login.html')

def register_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return redirect('login') #redirige al login una vez registrado
    return render(request, 'register.html')

#CERRAR LA SESION DEL USUARIO
def cerrar(request):
    username = request.user.username
    password = request.user.password
    idusuario = request.user.id

    print("\033[35mlogout........."+username+"clave ="+str(password)+"id ="+str(idusuario)+"\033[0m")
    user = authenticate(request, username=username, password=password)

    #desconectamos al usuario
    logout(request)
    return redirect('/')

#------------------------------------------------------------------------------------------------

def habilidades(request):
    print("\033[35mHola estoy en habilidades\033[0m")
    #select * from Habilidades order by habilidad
    #habilidades es un objeto de tipo queryset
    lista_habilidades = Habilidad.objects.all().order_by()
    #Habilidad se encuentra en models.py
    page = request.GET.get('page')
    paginator = Paginator(lista_habilidades, 2)

    if page == None:
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages
        request.session["pagina"] = page
    else:
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))

    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session:  # --> preguntamos si existe la variable
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_habilidades = paginator.get_page(page)
    except PageNotAnInteger:
        lista_habilidades = paginator.page(1)
    except EmptyPage:
        lista_habilidades = paginator.page(paginator.num_pages)

    #habilidades=Habilidad.objects.all().order_by('habilidad')
    #context = {'habilidades': habilidades} #esto era lo anterior

    context = {'lista_habilidades':lista_habilidades}
    return render(request, 'habilidades.html', context=context)

def ver_habilidad(request, id):
    print("ver habilidad")
    habilidad = Habilidad.objects.get(id=id)
    context = {'habilidad': habilidad}
    return render(request, 'ver_habilidad.html',context=context)

#profe 10/10/24
def eliminar_habilidad(request, eh):
    print("eliminar habilidad")
    expe_id=eh
    habilidad=Habilidad.objects.get(id=expe_id)

    if request.method == 'POST':
        habilidad.delete()
        return redirect('habilidades')

    return render(request, 'eliminar_habilidad.html', {'habilidad': habilidad})

#basandonos en lo que paso el profe
def editar_habilidad(request, mh):
    expe_id=mh
    habilidad = Habilidad.objects.get(id=expe_id)

    if request.method == 'POST':
        habilidad.habilidad = request.POST.get('habilidad')
        habilidad.nivel = request.POST.get('nivel')
        habilidad.save()
        return redirect('habilidades')  # Redirige a la lista de habilidades o a otra página

    return render(request, 'editar_habilidad.html', {'habilidad': habilidad})


def crear_habilidad(request):

    if request.method == 'POST':
        habilidad = request.POST.get('habilidad') #importante
        nivel = request.POST.get('nivel')

        habilidad = Habilidad(habilidad=habilidad, nivel=nivel)#ESTO CREA EL NUEVO OBJETO
        habilidad.save()
        return redirect('habilidades')  # Redirige a la lista de personas o a otra página

    return render(request, 'crear_habilidad.html') #NO NECESITA CONTEXTO PORQUE NO DEVUELVE NADA

#------------------------------------------------------------------------------------------------
#categorias pasadas por el profe
def categorias(request):
    lista_categorias = Categoria.objects.all()  # select * from Experiencias;
    page = request.GET.get('page') # --> actuara de boookmark (marcapáginas)
    paginator = Paginator(lista_categorias, 5)  # 5 registros por página

    if page == None:
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages #--> variable para todas las páginas
        #(ejemplo: iniciar sesion en iberia, y que tu nombre este visible todo el rato)
        #variable de sesión
        request.session["pagina"] = page
    else:
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))

    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session: # --> preguntamos si existe la variable
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_categorias = paginator.get_page(page)
    except PageNotAnInteger:
        lista_categorias = paginator.page(1)
    except EmptyPage:
        lista_categorias = paginator.page(paginator.num_pages)

    context = {'lista_categorias': lista_categorias}
    return render(request, 'categorias.html', context=context)

#------------------------------------------------------------------------------------------------
#hecha por mi (ejercicio clase)
def estudios(request):
    lista_estudios = Estudio.objects.all()
    page = request.GET.get('page')  #marcapáginas
    paginator = Paginator(lista_estudios, 1)  # 3 registros por página

    if page == None:
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages  # --> variable para todas las páginas
        request.session["pagina"] = page
    else:
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))

    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session:  # --> preguntamos si existe la variable
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_estudios = paginator.get_page(page)
    except PageNotAnInteger:
        lista_estudios = paginator.page(1)
    except EmptyPage:
        lista_estudios = paginator.page(paginator.num_pages)

    total_estudios = len(lista_estudios)

    context = {'lista_estudios':lista_estudios}
    return render(request, 'estudios.html', context=context)

#------------------------------------------------------------------------------------------------
# la dio el profe - 08/10/24
# experiencias != ver_experiencia
def experiencias(request):
    lista_experiencias = Experiencia.objects.all()  # MODELS.PY #QUERYSET
    page = request.GET.get('page')  # --> actuara de boookmark (marcapáginas)
    paginator = Paginator(lista_experiencias, 1)

    if page == None:
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages
        request.session["pagina"] = page
    else:
        print(" page recibe esle del none de get o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))

    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session:  # --> preguntamos si existe la variable
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_experiencias = paginator.get_page(page)
    except PageNotAnInteger:
        lista_experiencias = paginator.page(1)
    except EmptyPage:
        lista_experiencias = paginator.page(paginator.num_pages)

    context = {'lista_experiencias': lista_experiencias}
    return render(request, 'experiencias.html', context=context)
# experiencias.html???

# lo paso el profe
def ver_experiencia(request,id):
    expe_id=id
    experiencia = Experiencia.objects.get(id=expe_id)
    context = {'experiencia': experiencia}
    return render(request, 'ver_experiencia.html',context=context)

#profe 10/10/24
def eliminar_experiencia(request,pk):
    print("ELIMINAR")
    expe_id=pk
    experiencia = Experiencia.objects.get(id=expe_id)

    if request.method == 'POST':
        experiencia.delete()
        return redirect('experiencias.html')

    return render(request, 'eliminar_experiencia.html', {'experiencia':experiencia})

#------------------------------------------------------------------------------------------------
#31/10/2024
def subir_imagenes(request):
    idUsuario = request.session['idusuario']

    if request.method == 'POST':
        imagenes = request.FILES.getlist('imagenes')

        for imagen in imagenes:
            if imagen.name.endswith(('.png', '.jpg', '.jpeg', '.gif', '.jfif')):
                img = Imagen()
                img.imagen = imagen
                img.save()
        return redirect('subir_imagenes')

    vimagenes = Imagen.objects.all()
    return render(request, 'subir_imagenes.html', {'imagenes': vimagenes})

#04/11/2024
def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)

    if request.method == 'POST':
        imagen.delete()
        return redirect('subir_imagenes') #redirige a la galería de imágenes
    return redirect('subir_imagenes') #redirige a la galeria de imágenes

def editar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)

    if request.method == 'POST' and request.FILES.get('nueva_imagen'):
        # actualizamos la imagen
        imagen.imagen = request.FILES['nueva_imagen']
        imagen.save()
        return redirect('subir_imagenes') #redirige a la galeria de imágenes
    return redirect('subir_imagenes') #redirige a la galeria de imágenes

#------------------------------------------------------------------------------------------------
#31/10/2024
def subir_videos(request):
    if request.method == 'POST' and request.FILES['videos']:
        videos = request.FILES.getlist('videos')

        for video in videos:
            if video.name.endswith(('.mp3', '.mp4', '.mov', '.avi', '.mkv')):
                v=Video()
                v.video=video
                v.save()
        return redirect('subir_videos')

    vvideos = Video.objects.all()
    return render(request, 'subir_videos.html', {'videos': vvideos})

#04/11/2024
def eliminar_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST':
        video.delete()
        return redirect('subir_videos')
    return redirect('subir_videos')

def editar_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    if request.method == 'POST' and request.FILES.get('nuevo_video'):
        #actualizamos la imagen
        video.video = request.FILES['nuevo_video']
        video.save()
        return redirect('subir_videos')
    return redirect('subir_videos')

#------------------------------------------------------------------------------------------------

def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        context = {'nombre': nombre, 'email': email, 'asunto': asunto, 'mensaje': mensaje}
        template = render_to_string('email_template.html', context=context)

        email = EmailMessage(asunto, template, settings.EMAIL_HOST_USER, ['ashleychuquitarco2@gmail.com'])
        email.fail_silenty = False #que no marque error en gmail
        email.send()

        messages.success(request, "El mensaje se envió correctamente") #chatgpt
        return redirect('home')
    return render(request, 'correo.html')

#------------------------------------------------------------------------------------------------
#hecha por mi por aburrimiento
def empresa(request):
    DEBUG = "SI"
    print("Hola estoy en habilidades222"+str(DEBUG))
    empresas = Habilidad.objects.all().order_by('habilidad')
    context = {'empresas':empresas}
    return render(request, 'habilidades222.html', context=context)
