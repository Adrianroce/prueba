from django import forms
from Sesion.models import Image

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("user", "tipo", "img")
        widgets = { 
                   'user':forms.HiddenInput(),
                   'tipo':forms.HiddenInput()
                   }