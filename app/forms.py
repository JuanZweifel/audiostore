from .models import Categoria, Marca, Producto
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Cliente
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