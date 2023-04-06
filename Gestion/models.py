from django.db import models
from Sesion.models import Image
from django.conf import settings

# funciones
def get_img_profile(user_id):
    img_profile = Image.objects.filter(user=user_id, tipo='Profile_Image')

    if img_profile is not None and len(img_profile) > 0:
        return img_profile[0]
    else:
        return None
    

# MODELOS
class Ciudad(models.Model):
    ciudad_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    codigo = models.CharField(max_length=255, unique=True)
    familia = models.IntegerField()
    gastronomia = models.IntegerField()
    cultura = models.IntegerField()
    transporte = models.IntegerField()
    pareja = models.IntegerField()
    alojamiento = models.IntegerField()
    ocio = models.IntegerField()
    fiesta = models.IntegerField()

    def __str__(self):
        return self.nombre
    

class Ciudad_Mes(models.Model):
    ciudad_mes_id = models.AutoField(primary_key=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name="Meses")
    mes = models.IntegerField()

    def __str__(self):
        return f"{self.ciudad_id}: {self.mes}"

class Ciudad_Image(models.Model):
    imagen_id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='Image', default=None)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, related_name="Imagenes")


class Mensajes_Toast(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="toasts")
    mensaje_cabecera = models.CharField(max_length=255)
    mensaje_detalle = models.CharField(max_length=255)


# dto

class Ciudad_ImageDto():
    def __init__(self, img):
        if img is not None:
            self.imagen_id = img.imagen_id
            self.img = img.img
            self.ciudad = img.ciudad

class CiudadDto():
    def __init__(self, ciudad, img=None, meses=None, afinidad=None):
        self.ciudad_id = ciudad.ciudad_id
        self.nombre = ciudad.nombre
        self.codigo = ciudad.codigo
        self.familia = ciudad.familia
        self.gastronomia = ciudad.gastronomia
        self.cultura = ciudad.cultura
        self.transporte = ciudad.transporte
        self.pareja = ciudad.pareja
        self.alojamiento = ciudad.alojamiento
        self.ocio = ciudad.ocio
        self.fiesta = ciudad.fiesta
        self.img = Ciudad_ImageDto(img)
        self.meses = meses
        self.afinidad = afinidad

        # valoraciones
        valoraciones = [self.familia, self.gastronomia, self.cultura, self.transporte, self.pareja, self.alojamiento, self.ocio, self.fiesta]
        self.media_valoracion = int(sum(valoraciones)/len(valoraciones))

class UsuarioDto():
    def __init__(self, usuario):
        if usuario is not None:
            self.usuario_id = usuario.id 
            self.username = usuario.username
            self.img_profile = get_img_profile(usuario.id)
            self.seguidos = len(usuario.seguidos.all())
            self.seguidores = len(usuario.seguidores.all())

class Mensajes_ToastDto():
    def __init__(self, mt):
        if mt is not None:
            self.usuario = mt.usuario
            self.mensaje_cabecera = mt.mensaje_cabecera
            self.mensaje_detalle = mt.mensaje_detalle