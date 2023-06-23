from django import forms
from .models import Categoria, Marca, Producto

class frmProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ["nom_producto","precio","descripcion","stock","categoria_id","marca_id"]

class frmMarca(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["id_marca","nom_marca"]

class frmCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["id_cat","nom_cat"]