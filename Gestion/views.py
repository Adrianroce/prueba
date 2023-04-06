from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Gestion.models import Ciudad, Ciudad_Image, CiudadDto
from Gestion.models import get_img_profile, UsuarioDto, Mensajes_Toast, Mensajes_ToastDto
from Sesion.forms import ImageForm
from Sesion.models import Image
from django.contrib import messages
from Viaje.forms import ViajeForm, AnadirAmigosForm
from Viaje.models import Viaje, Viajero, ViajeDto
from Amigos.models import Relacion
from django.contrib.auth.models import User
from datetime import date

# funciones
def obtener_img_ciudad(ciudad_id):
    return Ciudad_Image.objects.filter(ciudad=ciudad_id).first()

def obtener_viajes_user(user, filtrar_fecha=True):
    hoy = date.today()

    if filtrar_fecha:
        # mostramos solo los viajes que no han terminado
        q = Viajero.objects.filter(usuario=user, viaje__fecha_fin__gt=hoy, viaje_aceptado=True)
    else:
        q = Viajero.objects.filter(usuario=user)

    viajeros = q.all()

    viajes = sorted([viaje.viaje for viaje in viajeros], key=lambda v: v.fecha_inicio)
    
    lst_viajes = []

    # obtengo los integrantes de cada viaje
    for v in viajes:
        
        viajeros = Viajero.objects.filter(viaje=v, viaje_aceptado=True)
        lst_viajes.append(ViajeDto(v, viajeros=viajeros))

    return lst_viajes

def obtener_viajes_no_aceptados_user(user, filtrar_fecha=True):
    hoy = date.today()

    if filtrar_fecha:
        # mostramos solo los viajes que no han terminado
        q = Viajero.objects.filter(usuario=user, viaje__fecha_fin__gt=hoy, viaje_aceptado=False)
    else:
        q = Viajero.objects.filter(usuario=user)

    viajeros = q.all()

    viajes = sorted([viaje.viaje for viaje in viajeros], key=lambda v: v.fecha_inicio)
    
    lst_viajes = []
    for v in viajes:
        
        viajeros = Viajero.objects.filter(viaje=v, viaje_aceptado=True)
        lst_viajes.append(ViajeDto(v, viajeros=viajeros))

    return lst_viajes

def obtener_solicitudes_amistad_pendientes(user):
    solicitudes_amistad_pend = Relacion.objects.filter(to_user=user, pendiente=True).all()

    return [UsuarioDto(s.from_user) for s in solicitudes_amistad_pend]

def obtener_toast_usuario(user):
    toasts = [Mensajes_ToastDto(t) for t in user.toasts.all()]

    # elimino los mensajes
    Mensajes_Toast.objects.filter(usuario=user).delete()

    return toasts

    

def getContext(request):
    ctx = {}
    viajes_por_aceptar = len(obtener_viajes_no_aceptados_user(request.user)) > 0
    ctx["viajes_no_aceptados"] = viajes_por_aceptar

    sol_pendiente = len(obtener_solicitudes_amistad_pendientes(request.user)) > 0
    ctx["solicitudes_no_resueltas"] = sol_pendiente

    toasts = obtener_toast_usuario(request.user)
    ctx["toasts"] = toasts

    return ctx

# funciones utiles
def obtenerepocameses(me):
    meses = set([1,2,3,4,5,6,7,8,9,10,11,12])
    a = me.split("|")
    c = set()
    for b in a:
        d = b.split(",")
        if len(d) == 1:
            c.add(d[0].strip())
        else:
            com = int(d[0].strip())
            fin = int(d[-1].strip())
            if com < fin:
                for i in range(int(com), int(fin)+1):
                    c.add(i)
            else:
                for i in meses.difference(set(list(range(int(fin)+1, int(com))))):
                    c.add(i)
    return c

def importar_imagenes_folder():
    import os
    from PIL import Image
    from io import BytesIO
    from django.core.files.base import ContentFile
    from django.core.files.uploadedfile import InMemoryUploadedFile

    base = '../cmd/imagenes/'
    ld = os.listdir(base)
    
    for im in ld:
        
        nombre = im.replace(".jpg", "")
        img = Image.open(f'{base}{im}')
        buffer = BytesIO()
        img.save(fp=buffer, format='JPEG')
        pillow_img = ContentFile(buffer.getvalue())

        ciudad = Ciudad.objects.filter(nombre=nombre)
        if len(ciudad) >0:
            ciudad = ciudad[0]
        else:
            ciudad = None
        if ciudad is not None:
            ciu = Ciudad_Image(ciudad=ciudad, img = InMemoryUploadedFile(
                pillow_img,       # file
                None,               # field_name
                im,           # file name
                'image/jpeg',       # content_type
                pillow_img.tell,  # size
                None) )
            ciu.save()
            
        

    

# vistas
@login_required
def home(request):
    ctx = getContext(request)
    #importar_imagenes_folder()
    ciudades = Ciudad.objects.all()
    imagenes = {}
    ciudades_dto = []
    # esto se puede mejorar haciendo una sola consulta en lugar de muchas
    for c in ciudades:
        ciu_img = obtener_img_ciudad(c.ciudad_id)
        ciu_dto = CiudadDto(c, img=ciu_img)
        ciudades_dto.append(ciu_dto)
    
        
    ctx['ciudades'] = ciudades_dto
    return render(request, 'home.html', ctx)

@login_required
def perfil(request):
    context = getContext(request)
    if request.method == "POST":
        pass
    else:
        img_profile = get_img_profile(request.user.id)
        context["img_profile"] = img_profile
    return render(request, 'perfil.html', context)

@login_required
def modificarPerfil(request):

    context = getContext(request)
    form = ImageForm(initial={'user': request.user.id, 'tipo':'Profile_Image'})
    context['form'] = form

    img_profile = get_img_profile(request.user.id)

    context["img_profile"] = img_profile
    
    if request.method == "POST":
        # actualizar info perfil

        return redirect('perfil')
    else:
        pass
        
    return render(request, 'perfil_edit.html', context)

@login_required
def modificarImgPerfil(request):
    context = getContext(request)
    img_profile = None
    if request.method == "POST":

        form = ImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            img_profile = get_img_profile(request.user.id)
            if img_profile is not None:
                img_profile.img = form.cleaned_data["img"]
                img_profile.save()
            else:
               form.save() 

            messages.success(request, "Imagen cargada con exito")
            return redirect('modificarPerfil')
        else:
            messages.error(request, "Error guardando imagen")
    else:
        img_profile = get_img_profile(request.user.id)

    context["img_profile"] = img_profile
    return render(request, 'perfil_edit.html', context)

@login_required
def misviajes(request):
    ctx = getContext(request)

    if request.method == "POST":
        pass
            
    else:
        pass

    viajes = obtener_viajes_user(request.user)

    # obtengo si el usuario es administrador o no de cada viaje
    for v in viajes:
        for vi in v.viajeros:
            if vi.usuario.usuario_id == request.user.id:
                v.usuario_admin = vi.administrador

    ctx["viajes"] = viajes

    return render(request, 'viajes.html', ctx)

@login_required
def amigos(request):
    ctx = getContext(request)
    sol_pendiente = obtener_solicitudes_amistad_pendientes(request.user)
    ctx["solicitudes_no_resueltas"] = sol_pendiente
    return render(request, 'amigos.html', ctx)

@login_required
def destinoDetalles(request, ciudad_id):
    ctx = getContext(request)

    if request.method == "POST":
        pass
    else:
        ciudad_destino = Ciudad.objects.filter(pk=ciudad_id).first()

        img = obtener_img_ciudad(ciudad_destino.ciudad_id)

        ctx["ciudad_destino"] = CiudadDto(ciudad_destino, img=img)

        form = ViajeForm(initial={'destino': ciudad_id})
        ctx['form'] = form
    
    return render(request, 'destino_detalle.html', ctx)



@login_required
def crearViaje(request):

    ctx = getContext(request)

    if request.method == "POST":
        form = ViajeForm(request.POST)
        
        if form.is_valid():
            # guardo el viaje
            descripcion = form.cleaned_data["descripcion"]
            presupuesto = form.cleaned_data["presupuesto"]
            fecha_inicio = form.cleaned_data["fecha_inicio"]
            fecha_fin = form.cleaned_data["fecha_fin"]
            dest = form.cleaned_data["destino"]

            destino = Ciudad.objects.filter(pk=dest).first()

            v = Viaje(descripcion=descripcion, presupuesto=presupuesto, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, destino=destino)
            v.save()

            # guardo viajero
            vi = Viajero(viaje=v, usuario=request.user, creador=True, administrador=True, viaje_aceptado=True)
            vi.save()

            messages.success(request, "Correcto")
            return redirect('viajestab')
        else:
            messages.error(request, "Error")
    else: 
        pass

@login_required 
def verViaje(request, viaje_id):
    ctx = getContext(request)
    v = Viaje.objects.filter(pk=viaje_id).first()
    viajeros = Viajero.objects.filter(viaje=v, viaje_aceptado=True)
    viaje = ViajeDto(v, viajeros=viajeros)

    ctx["viaje_modificar"] = viaje
    return render(request, 'viaje_edit_modal.html', ctx)

@login_required 
def modificarViaje(request):
    ctx = getContext(request)

    return render(request, 'viajes.html', ctx)

@login_required
def amigosBuscar(request, viaje_id):
    ctx = getContext(request)

    # mostrare solo aquellos usuarios que njo estan incluidos ya en el viaje
    # obtengo viaje
    viaje = Viaje.objects.filter(pk=viaje_id).first()

    # viajeros del viaje ya unidos o invitados
    viajeros = viaje.integrantes.all()
    usuarios_unidos = [v.usuario.id for v in viajeros]

    # mostraremos solo los usuarios a los que sigue
    seguidos = request.user.seguidos.all()
    usuarios_seguidos_ids = [r.to_user.id for r in seguidos]

    # obtengo ususarios
    usuarios = User.objects.filter(pk__in=usuarios_seguidos_ids).exclude(pk__in=usuarios_unidos).all()

    ctx["usuarios"] = usuarios
    print(usuarios)
    ctx["viaje_id"] = viaje_id
    
    return render(request, 'viaje_amigos_buscar.html', ctx)


@login_required
def viajesGestionar(request):
    ctx = getContext(request)

    viajes_por_aceptar = obtener_viajes_no_aceptados_user(request.user)
    ctx["viajes_no_aceptados"] = viajes_por_aceptar

    return render(request, 'viajes_gestionar.html', ctx)

@login_required
def viajeAceptar(request, viaje_id):

    # se acepta el viaje
    viaje = Viaje.objects.filter(pk=viaje_id).first()
    v = Viajero.objects.filter(viaje=viaje, usuario=request.user).first()
    v.viaje_aceptado = True
    v.save()

    integrantes = [v.usuario for v in Viajero.objects.filter(viaje=viaje).exclude(usuario=request.user).all()]

    for i in integrantes:
        m = Mensajes_Toast(usuario=i, 
                           mensaje_cabecera=f"Viaje a {viaje.destino.nombre}",
                           mensaje_detalle=f"{request.user.username} se ha unido al viaje!!")
        m.save()

    return redirect('viajesGestionar')

@login_required
def viajeRechazar(request, viaje_id):
    
    # se elimina el registro viajero del viaje
    viaje = Viaje.objects.filter(pk=viaje_id).first()
    viajero = Viajero.objects.filter(viaje=viaje, usuario=request.user).all()

    # elimino todos los registros si existen mas de uno
    for v in viajero:
        v.delete()

    return redirect('viajesGestionar')

@login_required
def seguidos(request):
    ctx = getContext(request)
    # obtengo los usuarios a los que sigue
    seguidos = Relacion.objects.filter(from_user=request.user, pendiente=False).all()

    ctx["seguidos"] = [UsuarioDto(s.to_user) for s in seguidos]

    sol_pendiente = obtener_solicitudes_amistad_pendientes(request.user)
    ctx["solicitudes_no_resueltas"] = sol_pendiente
    
    return render(request, 'seguidos.html', ctx)

@login_required
def seguidores(request):
    ctx = getContext(request)
    # obtengo los usuarios que le siguen
    seguidores = Relacion.objects.filter(to_user=request.user, pendiente=False).all()

    ctx["seguidores"] = [UsuarioDto(s.from_user) for s in seguidores]
    
    return render(request, 'seguidores.html', ctx)

@login_required
def amigosSolicitudes(request):
    ctx = getContext(request)
    # obtengo los usuarios que le siguen pero aun no esta aceptadaa la solicitud
    

    ctx["solicitudes_amistad_pend"] = obtener_solicitudes_amistad_pendientes(request.user)
    
    return render(request, 'solicitudes_amistad_pend.html', ctx)

@login_required
def amigoAceptar(request, amigo_id):
    

    # se acepta la solicitud
    amigo = User.objects.filter(pk=amigo_id).first()
    v = Relacion.objects.filter(from_user=amigo, to_user=request.user).first()
    v.pendiente = False
    v.save()
    
    messages.success(request, "Solicitud aceptada correctamente")

    if len(obtener_solicitudes_amistad_pendientes(request.user)) > 0:
        return redirect('amigosSolicitudes')
    else:
        return redirect('seguidores')

@login_required
def amigoRechazar(request, amigo_id):
    
    # se elimina el registro de la solicitud
    amigo = User.objects.filter(pk=amigo_id).first()
    rel = Relacion.objects.filter(from_user=amigo, to_user=request.user).all()

    # elimino todos los registros si existen mas de uno
    for v in rel:
        v.delete()

    messages.success(request, "Solicitud rechazada correctamente")

    if len(obtener_solicitudes_amistad_pendientes(request.user)) > 0:
        return redirect('amigosSolicitudes')
    else:
        return redirect('seguidores')
    
@login_required
def amigosAgregar(request):
    ctx = getContext(request)

    # mostrare solo aquellos usuarios que no se siguen ya
    # excluidmos los usuarios a los que sigue
    seguidos = request.user.seguidos.all()
    usuarios_seguidos_ids = [r.to_user.id for r in seguidos]
    usuarios_seguidos_ids.append(request.user.id) # tampoco tiene que aparecer el propio usuario

    # obtengo ususarios
    usuarios = User.objects.exclude(pk__in=usuarios_seguidos_ids).all()

    ctx["usuarios"] = usuarios
    
    return render(request, 'amigos_buscador.html', ctx)

@login_required
def SeguirUsuarios(request):
    context = getContext(request)
    if request.method == "POST":
        lista_usuarios_seguir = request.POST.getlist('checks')
        if len(lista_usuarios_seguir) > 0:

            # usuarios ya seguidos
            usuarios_seguidos_rel = request.user.seguidos.all()
            usuarios_seguidos = [v.to_user.id for v in usuarios_seguidos_rel]

            # obtengo ususarios
            usuarios = User.objects.filter(pk__in=lista_usuarios_seguir).exclude(pk__in=usuarios_seguidos).all()

            # añado los usuarios al viaje
            for usuario in usuarios:
                r = Relacion(from_user=request.user, to_user=usuario, fecha=date.today(), pendiente=True)
                r.save()

            messages.success(request, "Usuarios seguidos correctamente")
        else:
            messages.error(request, "Error siguiendo usuarios")
    else:
        pass
    
    return redirect('seguidos')