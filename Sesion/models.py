from django.db import models
from django.conf import settings

class Image(models.Model):
    imagen_id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to='Image', default=None)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)

