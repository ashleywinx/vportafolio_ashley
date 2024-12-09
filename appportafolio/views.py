# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404 #
from django.http import HttpResponse
from appportafolio.models import *
from .models import Tarea , Estado # models.py
from .forms import TareaForm  # Importa el formulario desde forms.py
from .models import Trabajo, Calificacion

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
from pportafolio.wsgi import application #no lo tiene el profe, pero si lo esta usando el programa

#PDF'S 08/11/2024
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors #para los colores del pdf

#curriculum con reportlab 14/11/24
from reportlab.lib.utils import ImageReader
import os

#para el chat
from django.http import JsonResponse

#------------------------------------------------------------------------------------------------
# Create your views here.
from datetime import datetime
from django.utils import timezone

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
#profe 17/10/2024 "ENTREVISTADORES"
def login_view(request):
    print("\033[35mlogin_view\033[0m")

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            actual=request.user #usuario actual
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

#----- 08/11/2024 -----------------------------------------------
# controlador de la vista para montar la lista de entrevistadores.
def listar_entrevistadores(request):
    entrevistadores = Entrevistador.objects.all()
    return render(request, 'listar_entrevistadores.html', {'entrevistadores': entrevistadores})

def generar_pdf(request, entrevistador_id):
    entrevistador = Entrevistador.objects.get(id=entrevistador_id)

    # Crear una respuesta HTTP con contenido tipo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="entrevistador_{entrevistador.id}.pdf"'

    # Crear el objetp canvas de Reportlab
    p = canvas.Canvas(response, pagesize=letter)

    # Configuración del titulo
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(300, 770, "Reporte de Entrevistador")

    # Volver al tamaño de fuente normal
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)

    # Datos del entrevistador
    p.drawString(100, 720, f"ID: {entrevistador.id}")
    p.drawString(100, 700, f"Empresa: {entrevistador.empresa or 'N/A'}")
    p.drawString(100, 680, f"Fecha de Entrevista: {entrevistador.fecha_entrevista or 'N/A'}")
    p.drawString(100, 660, f"Conectado: {'Si' if entrevistador.conectado else 'No'}")
    p.drawString(100, 640, f"Seleccionado: {'Si' if entrevistador.seleccionado else 'No'}")
    p.drawString(100, 620, f"Usuario: {entrevistador.user.username if entrevistador.user else 'N/A'}")

    # Añadir avatar si existe
    if entrevistador.avatar:
        avatar_path = entrevistador.avatar.path
        p.drawImage(avatar_path, 100, 500, width=100, height=100)

    # Guardar el PDF
    p.showPage()
    p.save()

    return response

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
        #(ejemplo: iniciar sesion en iberia, y que tu nombre este visible all el rato)
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
            if imagen.name.endswith(('.png', '.PNG', '.jpg', '.JPG', '.jpeg', '.JPEG', '.gif', '.GIF', '.jfif', '.JFIF')):
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
            if video.name.endswith(('.mp3', '.MP3', '.mp4', '.MP4', '.mov', '.MOV', '.avi', '.AVI', '.mkv', '.MKV')):
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

        email_message = EmailMessage(asunto, template, settings.EMAIL_HOST_USER, [email])
        email_message.fail_silenty = False #que no marque error en gmail
        email_message.send()

        messages.success(request, "El mensaje se envió correctamente")
        return redirect('home')
    return render(request, 'correo.html')

#------------------------------------------------------------------------------------------------
#vista para gregar un curriculum (solo teléfono y email) 14/11/24
def agregar_curriculum(request):
    if request.method == 'POST':
        personal_id = request.POST.get('personal_id')
        nombre = request.POST.get('nombre')
        ap1 = request.POST.get('ap1')
        ap2 = request.POST.get('ap2')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        # Obtener o crear un objeto de Personal
        personal, created = Personal.objects.get_or_create(
            nombre=nombre, apellido1=ap1, apellido2=ap2
        )

        # Crear un nuevo objeto Curriculum, asignando el objeto Personal
        curriculum = Curriculum(
            personal=personal,  # Relación con el objeto Personal
            email=email,
            telefono=telefono
        )
        curriculum.save()

        return redirect('ver_curriculum', pk=curriculum.pk)
    return render(request, 'agregar_curriculum.html')

#Vista para ver un curriculum
def ver_curriculum(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    estudios = DetalleCurriculumEstudio.objects.filter(curriculum=curriculum)
    experiencias = DetalleCurriculumExperiencia.objects.filter(curriculum=curriculum)

    context = {'curriculum': curriculum, 'estudios': estudios, 'experiencias': experiencias}
    return render (request, 'ver_curriculum.html', context=context)

#El controlador que genera el pdf
def generar_pdf(request, entrevistador_id):
    curriculum = get_object_or_404(Curriculum, id=entrevistador_id)
    estudios = DetalleCurriculumEstudio.objects.filter(curriculum=curriculum)
    experiencias = DetalleCurriculumExperiencia.objects.filter(curriculum=curriculum)

    #crear la respuesta HttpResponse con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="curriculum_{curriculum.personal.nombre}_{curriculum.personal.apellido1}.pdf"'

    #crear un objeto canvas de ReportLab para generar el PDF
    c = canvas.Canvas(response, pagesize=letter)
    width, height=letter #tamaño de la página

    #cargar imagen de avatar
    try:
        avatar_path = "C:/vportafolio/pportafolio/static/images/chica3.jpg"
        #avatar_path = "C:/vportafolio/pportafolio/media/MEDIA/moneda3.jpg"
        #avatar_path = os.path.join(settings.MEDIA_ROOT, "MEDIA/moneda3.jpg")
        avatar = ImageReader(avatar_path)
        c.drawImage(avatar, width - 150, height - 150, width=100, height=100)
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
        pass #si no se encuentra la imagen, el PDF se generará sin ella

    #Titulo del currículum en color
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#4B8BBE")) #cambia a cualquier color hex que prefieras
    c.drawString(100, height -100, f"Curriculum de {curriculum.personal.nombre} {curriculum.personal.apellido1}")

    #Información de contacto en color diferente
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#306998")) #otro color para variar
    c.drawString(100, height -130, f"Email: {curriculum.email}")
    c.drawString(100, height -150, f"Teléfono {curriculum.telefono}")

    #seccion de estudios en otro color
    y_position = height -200
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#FFD43B"))
    c.drawString(100, y_position, "Estudios:")

    #mostrar cada estudio con detalles
    c.setFont("Helvetica", 12)
    y_position -= 20

    for estudio in estudios:
        c.setFillColor(colors.black)
        c.drawString(100, y_position, f"{estudio.estudio.titulacion} en {estudio.estudio.nombreLugar} ({estudio.estudio.fecha_inicio} - {estudio.estudio.fecha_fin})")
        #c.drawString(100, y_position, f"{estudio.titulo} en {estudio.nombreLugar} ({estudio.fecha_inicio} - {estudio.fecha_fin})")
        y_position -= 20

    #seccion de experiencia laboral
    y_position -= 40
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#306998"))
    c.drawString(100, y_position, "Experiencia laboral:")

    y_position -= 20
    c.setFont("Helvetica", 12)

    for experiencia in experiencias:
        c.setFillColor(colors.blank)
        c.drawString(100, y_position, f"{experiencia.categoria} en {experiencia.empresa} ({experiencia.fecha_inicio} - {experiencia.fecha_fin})")
        y_position -= 20

    #finalizar el PDF
    c.showPage() #si tienes más páginas
    c.save()

    return response

#------------------------------------------------------------------------------------------------
#vista para ver las noticias 18/11/24
def lista_noticias(request):
    noticias = Noticia.objects.all().order_by('-fecha_creacion')
    return render(request, 'lista_noticias.html', {'noticias': noticias})

#vista para crear una nueva noticia
def crear_noticia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')

        if titulo and contenido:
            noticia = Noticia.objects.create(titulo=titulo, contenido=contenido, imagen=imagen)
            return redirect('lista_noticias')
        else:
            return HttpResponse("ERROR: El título y el contenido son obligatorios.", status=400)

    return render(request, 'crear_noticia.html')

#------20-11-24--------valoración-con-estrellas--------------------------------------------------
def listar_valoraciones(request):
    valoraciones = Valoracion.objects.all()
    return render(request, 'List.html', {'valoraciones': valoraciones})

def actualizar_valoracion(request, pk):
    valoracion = get_object_or_404(Valoracion, pk=pk)

    if request.method == 'POST':
        # Obtener valores enviados en el formulario
        votos_entrevista = int(request.POST.get('votos_entrevista', valoracion.votos_entrevista))
        votos_empresa = int(request.POST.get('votos_empresa', valoracion.votos_empresa))

        # Actualizar los campos de la valoración #Actualizar los votos y recalcular la media
        valoracion.votos_entrevista = votos_entrevista
        valoracion.votos_empresa = votos_empresa
        valoracion.media_aspectos = (votos_entrevista) + float(votos_empresa) / 2
        valoracion.save()
        return redirect('listar_valoraciones')

    return render(request, 'update.html', {'valoracion': valoracion})

def añadir_valoracion(request):

    if request.method == 'POST':
        entrevista = request.POST.get('entrevista')
        empresa = request.POST.get('empresa')
        votos_entrevista = int(request.POST.get('votos_entrevista', 0))
        votos_empresa = int(request.POST.get('votos_empresa', 0))

        # Calcular la media de los aspectos
        media_aspectos = (votos_entrevista + votos_empresa) / 2

        # Crear y guardar la nueva valoración
        nueva_valoracion = Valoracion.objects.create(
            entrevista = entrevista,
            empresa = empresa,
            votos_entrevista = votos_entrevista,
            votos_empresa = votos_empresa,
            media_aspectos = media_aspectos
        )

        return redirect('listar_valoraciones')

    return render(request, 'add.html')

#-------------------22-11-24- lo paso el profe ---------------------------------------------------
@login_required
def seleccionar_entrevistadores(request):
    entrevistadores = Entrevistador.objects.all()
    # Si el usuario está enviando un formulario, redirigir al chat con el entrevistador seleccionado
    if request.method == 'POST':
        entrevistador_id = request.POST.get('entrevistador_id')
        return redirect('chat_view', entrevistador_id=entrevistador_id)
    return render(request, 'seleccionar_entrevistador.html', {'entrevistadores': entrevistadores})

#------------------- yo en casa -------------
@login_required
def chat_view(request, entrevistador_id):
    entrevistador = get_object_or_404(Entrevistador, id=entrevistador_id)

    mensajes = Mensaje.objects.filter(
        (models.Q(remitente=request.user) & models.Q(destinatario=entrevistador.user)) |
        (models.Q(remitente=entrevistador.user) & models.Q(destinatario=request.user))
    )

    # agregar la propiedad 'clase' para usarla en el template
    for mensaje in mensajes:
        mensaje.clase = 'enviado' if mensaje.remitente == request.user else 'recibido'

    # renderizar solo el chat para la respuesta AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'mensajesHtml': render_to_string('chat_mensajes.html', {'mensajes': mensajes})  # ,
        })

    return render(request, 'chat.html', {'entrevistador': entrevistador, 'mensajes': mensajes})

# ---------------------------------------------------------------------------------------------------
@login_required
def enviar_mensaje(request):
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        destinatario_id = request.POST.get('destinatario_id')
        destinatario = get_object_or_404(User, id=destinatario_id)

        mensaje = Mensaje.objects.create(
            remitente = request.user,
            destinatario = destinatario,
            contenido = contenido
        )
        return JsonResponse({'status': 'success', 'mensaje': mensaje.contenido, 'fecha_envio': mensaje.fecha_envio})

    return JsonResponse({'status': 'error', 'mensaje': 'Método no permitido'})

#------------------------------------------------------------------------------------------------
def crear_noticia1(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_noticias')
        else:
            form = NoticiaForm()
    return render(request, 'crear_noticia1.html', {'form': form})

#-------------- calificaciones ---------------------------------------------------------------------------
def listar_calificaciones(request):
    calificaciones = Calificacion.objects.all().order_by('nota')
    totalMedia = 0
    i = 0
    for media in calificaciones:
        totalMedia = totalMedia + media.nota
        i = i + 1
    totalMedia = totalMedia/i
    return render(request, "lista_calificaciones.html", {'calificaciones':calificaciones, 'totalMedia':totalMedia})

def añadir_calificacion(request):
    if request.method == "POST":
        asignatura = request.POST.get('asignatura')
        nota = int(request.POST.get('nota',0))

        #Crear y guardar nueva calificacion
        nueva_calificacion = Calificacion.objects.create(
            asignatura = asignatura,
            nota = nota,
        )
        return redirect('listar_calificaciones')
    return render(request, 'añadir_calificacion.html')

#-------------- TAREAS ---------------------------------------------------------------------------
def lista_tareas(request):
    tareas = Tarea.objects.all()
    return render(request, 'lista_tareas.html', {'tareas': tareas})

def crear_tarea(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')  # Redirige a la lista de tareas
    else:
        form = TareaForm()
    return render(request, 'crear_tarea.html', {'form': form})

def actualizar_evento(request, evento_id):
    evento = get_object_or_404(Tarea, id=evento_id)
    estados = Estado.objects.all()

    if request.method == 'POST':
        tarea = request.POST.get('nombre')
        fecha_hora = request.POST.get('fecha_tarea')
        fkestado_id = request.POST.get('fkestado')

        # Actualiza los campos del modelo
        evento.tarea = tarea
        evento.fecha_tarea = fecha_hora
        evento.fkestado_id = fkestado_id
        evento.save()

        return redirect('lista_tareas')

    return render(request, 'actualizar.html', {'evento': evento, 'estados': estados})

#------------------------------------------------------------------------------------------------
def lista_proyectos(request):
    proyectos = Trabajo.objects.all()
    return render(request, 'lista_proyectos.html', {'proyectos':proyectos})

def crear_proyecto(request):
    if request.method == 'POST':
        print(request.POST)
        titulo = request.POST.get('titulo')
        lenguaje = request.POST.get('lenguaje')
        tecnologias = request.POST.get('tecnologias')
        observaciones = request.POST.get('observaciones')
        fecha_proyecto = request.POST.get('fecha_proyecto')

        if titulo and fecha_proyecto:
            trabajo = Trabajo.objects.create(
                titulo=titulo,
                lenguaje=lenguaje,
                tecnologias=tecnologias,
                observaciones=observaciones,
                fecha_proyecto=fecha_proyecto,
            )
            return redirect('lista_proyectos')
        else:
            return HttpResponse("ERROR: El título y la fecha son obligatorios.", status=400)
    return render(request, 'crear_proyecto.html')

#------------------------------------------------------------------------------------------------
#hecha por mi por aburrimiento
def empresa(request):
    DEBUG = "SI"
    print("Hola estoy en habilidades222"+str(DEBUG))
    empresas = Habilidad.objects.all().order_by('habilidad')
    context = {'empresas':empresas}
    return render(request, 'habilidades222.html', context=context)
