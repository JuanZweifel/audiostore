from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
validarletras = RegexValidator(r'^[a-zA-ZñÑ]*$', 'Ingrese solo letras y sin espacios')
class Categoria(models.Model):
    id_cat=models.AutoField(primary_key=True, null=False)
    nom_cat=models.CharField(max_length=50, null=False)
    
    def __str__(self):
        return self.nom_cat

class Marca(models.Model):
    id_marca=models.AutoField(primary_key=True, null=False)
    nom_marca=models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.nom_marca

class Producto(models.Model):
    id_producto = models.AutoField(primary_key= True, null=False)
    nom_producto = models.CharField(max_length=50, null=False)
    precio = models.IntegerField(null=False)
    descripcion = models.TextField(null=True)
    stock = models.IntegerField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)

class ImagenProducto(models.Model):
    id_imagen=models.AutoField(primary_key=True)
    imagen = models.ImageField(null=False, blank=True, upload_to="Productos", height_field=None, width_field=None, max_length=None)
    producto = models.ForeignKey(Producto, on_delete= models.CASCADE, related_name="imagenes")
    def __str__(self):
        return f"{self.imagen}"


class Cliente(models.Model):
    
    
    usuario=models.OneToOneField(User, unique=True, related_name='perfil', on_delete=models.CASCADE)
    
    run=models.CharField(primary_key=True, null=False, max_length=10)   
    primer_nombre=models.CharField(max_length=30, null=False, validators=[validarletras])
    segundo_nombre=models.CharField(max_length=30, null=False, validators=[validarletras])
    apellido_paterno=models.CharField(max_length=30, null=False, validators=[validarletras])
    apellido_materno=models.CharField(max_length=30, null=False, validators=[validarletras])
    correo=models.EmailField(max_length=254, unique=True)

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    id_producto = models.IntegerField(null=True)
    img = models.ImageField(null=True)
    producto = models.CharField(max_length=50, null=False)
    precio = models.IntegerField(null=False)
    cantidad = models.IntegerField(null=False)

class Pedido(models.Model):
    ESTADO = [
        ("R","Retirado"),("NR","No Retirado")
    ]
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    estado = models.CharField(null=False, choices=ESTADO, max_length=50, default="No Retirado")

class DetallePedido(models.Model):
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE)
    id_producto = models.IntegerField(null=True)
    producto = models.CharField(max_length=50, null=False)
    precio = models.IntegerField(null=False)
    cantidad = models.IntegerField(null=False)