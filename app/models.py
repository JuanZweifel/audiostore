from django.db import models

# Create your models here.
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
    descripcion = models.TextField(max_length=300, null=False)
    stock = models.IntegerField(null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    
    
class ImagenProducto(models.Model):
    id_imagen=models.AutoField(primary_key=True)
    imagen = models.ImageField(null=False, blank=True, upload_to="Productos", height_field=None, width_field=None, max_length=None)
    producto = models.ForeignKey(Producto, on_delete= models.CASCADE, related_name="imagenes")
    def __str__(self):
        return f"{self.imagen}"