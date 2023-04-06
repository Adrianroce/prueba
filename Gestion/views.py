from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Gestion.models import Ciudad, Ciudad_Image, CiudadDto
from Gestion.models import get_img_profile, UsuarioDto, Mensajes_Toast, Mensajes_ToastDto
from Sesion.forms import ImageForm
from Sesion.models import Image
from django.contrib import messages
#from Viaje.forms import ViajeForm, AnadirAmigosForm
#from Viaje.models import Viaje, Viajero, ViajeDto
#from Amigos.models import Relacion
from django.contrib.auth.models import User
from datetime import date

# funciones
def obtener_img_ciudad(ciudad_id):
    return Ciudad_Image.objects.filter(ciudad=ciudad_id).first()

# falta

    

def getContext(request):
    ctx = {}
    #falta

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
    #falta
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

    #falta

    return render(request, 'viajes.html', ctx)

@login_required
def amigos(request):
    ctx = getContext(request)
    #falta
    #sol_pendiente = obtener_solicitudes_amistad_pendientes(request.user)
    #ctx["solicitudes_no_resueltas"] = sol_pendiente
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

        #form = ViajeForm(initial={'destino': ciudad_id})
        #ctx['form'] = form
    
    return render(request, 'destino_detalle.html', ctx)



@login_required
def crearViaje(request):

    ctx = getContext(request)

    #falta

@login_required 
def verViaje(request, viaje_id):
    ctx = getContext(request)
    #falta
    return render(request, 'viaje_edit_modal.html', ctx)

@login_required 
def modificarViaje(request):
    ctx = getContext(request)

    return render(request, 'viajes.html', ctx)

@login_required
def amigosBuscar(request, viaje_id):
    ctx = getContext(request)

    #falta
    
    return render(request, 'viaje_amigos_buscar.html', ctx)


@login_required
def viajesGestionar(request):
    ctx = getContext(request)

    #falta

    return render(request, 'viajes_gestionar.html', ctx)

@login_required
def viajeAceptar(request, viaje_id):

    #falta

    return redirect('viajesGestionar')

@login_required
def viajeRechazar(request, viaje_id):
    
    #falta

    return redirect('viajesGestionar')

@login_required
def seguidos(request):
    ctx = getContext(request)
    # obtengo los usuarios a los que sigue
    #falta
    
    return render(request, 'seguidos.html', ctx)

@login_required
def seguidores(request):
    ctx = getContext(request)
    #falta
    
    return render(request, 'seguidores.html', ctx)

@login_required
def amigosSolicitudes(request):
    ctx = getContext(request)
    #falta
    
    return render(request, 'solicitudes_amistad_pend.html', ctx)

@login_required
def amigoAceptar(request, amigo_id):
    

    #falta

    if 1 > 0: #falta
        return redirect('amigosSolicitudes')
    else:
        return redirect('seguidores')

@login_required
def amigoRechazar(request, amigo_id):
    
   #falta

    if 1 > 0:#falta
        return redirect('amigosSolicitudes')
    else:
        return redirect('seguidores')
    
@login_required
def amigosAgregar(request):
    ctx = getContext(request)

    #falta
    
    return render(request, 'amigos_buscador.html', ctx)

@login_required
def SeguirUsuarios(request):
    context = getContext(request)
    #falta
    
    return redirect('seguidos')