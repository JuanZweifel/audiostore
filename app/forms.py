from django import forms
from .models import Categoria, Marca, Producto
from django.core.validators import MaxValueValidator, MinValueValidator

class frmPago(forms.Form):
    CHOICES = [
        ("Tarjeta de credito", "Tarjeta de credito"),
        ("Tarjeta de debito", "Tarjeta de debito"),
        ("PayPal", "PayPal")
    ]
    tipo_pago = forms.ChoiceField(label="Tipo de pago", widget=forms.RadioSelect,choices=CHOICES, required=True)
    nombre_titular = forms.CharField(label="Nombre del titular", max_length=150, required=True)
    numero_titular = forms.IntegerField(label="Número de la tarjeta", required=True)
    expiracion = forms.IntegerField(label="Expiración ", required=True)
    cvv = forms.IntegerField(label="CVV", required=True, validators=[MinValueValidator(0),MaxValueValidator(999)])