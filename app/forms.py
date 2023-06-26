from django import forms
from .models import Producto, ImagenProducto
from django.forms import formset_factory

class frmProducto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ["id_producto","nom_producto","precio","descripcion","stock","categoria","marca"]
        

class frmImagen(forms.ModelForm):
    
    class Meta:
        model = ImagenProducto
        fields = ["imagen"]


ImageFormSet = formset_factory(frmImagen, extra=0,max_num=5, can_delete=True, can_delete_extra=True)