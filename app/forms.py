from .models import Categoria, Marca, Producto
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente
from django import forms
from .models import Producto, ImagenProducto
from django.forms import formset_factory
class LoginForm(AuthenticationForm):
    pass

class frmCrearCuenta(UserCreationForm):
    class Meta:
        model=User
        fields=["username","password1","password2"]
        
class frmPerfilCliente(forms.ModelForm):

    class Meta:
        model=Cliente
        fields=["run","primer_nombre","segundo_nombre","apellido_paterno","apellido_materno","correo"]
        
class frmModifDatosCliente(forms.ModelForm):
    
    class Meta:
        model=Cliente
        fields=["primer_nombre","segundo_nombre","apellido_paterno","apellido_materno","correo"]

class frmPago(forms.Form):
    CHOICES = [
        ("Tarjeta de credito", "Tarjeta de credito"),
        ("Tarjeta de debito", "Tarjeta de debito"),
        ("PayPal", "PayPal")
    ]
    tipo_pago = forms.ChoiceField(label="Tipo de pago", widget=forms.RadioSelect,choices=CHOICES, required=True)
    numero_titular = forms.IntegerField(label="Número de la tarjeta", required=True)
    nombre_titular = forms.CharField(label="Nombre del titular", max_length=150, required=True)
    expiracion = forms.IntegerField(label="Expiración ", required=True)
    cvv = forms.IntegerField(label="CVV", required=True, validators=[MinValueValidator(0),MaxValueValidator(999)])

class frmProducto(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ["id_producto","nom_producto","precio","descripcion","stock","categoria","marca"]
        

class frmImagen(forms.ModelForm):
    
    class Meta:
        model = ImagenProducto
        fields = ["imagen"]

class frmCategoria(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["id_cat", "nom_cat"]
        
        
class frmMarca(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ["id_marca", "nom_marca"]

ImageFormSet = formset_factory(frmImagen, extra=0,max_num=5, can_delete=True, can_delete_extra=True)