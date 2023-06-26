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
