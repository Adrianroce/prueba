from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Gestion.models import Ciudad, Ciudad_Image, CiudadDto
from Gestion.models import get_img_profile, UsuarioDto, Mensajes_Toast, Mensajes_ToastDto
from Sesion.forms import ImageForm
from Sesion.models import Image
from django.contrib import messages
from django.contrib.auth.models import User
from datetime import date


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
    ctx = {}
    #importar_imagenes_folder()
    ciudades = Ciudad.objects.all()
    imagenes = {}
    ciudades_dto = []
    # esto se puede mejorar haciendo una sola consulta en lugar de muchas
    
        
    ctx['ciudades'] = ciudades_dto
    return render(request, 'home.html', ctx)
