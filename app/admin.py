from django.contrib import admin
from app.models import Categoria, Producto, Marca, Carrito

# Register your models here.

class admCategoria(admin.ModelAdmin):
    list_display=["id_cat","nom_cat"]
    list_editable=["nom_cat"]
    class meta:
        model=Categoria

class admMarca(admin.ModelAdmin):
    list_display=["id_marca","nom_marca"]
    list_editable=["nom_marca"]
    class meta:
        model=Marca
        
        
class admProducto(admin.ModelAdmin):
    list_display=["id_producto", "nom_producto", "precio", "descripcion", "stock", "categoria", "marca"]
    list_editable=["nom_producto", "precio", "descripcion", "stock", "categoria", "marca"]
    class meta:
        model=Producto

class admCarrito(admin.ModelAdmin):
    list_display=["producto", "precio", "cantidad"]
    list_editable=["precio", "cantidad"]
    class meta:
        model=Carrito

admin.site.register(Categoria, admCategoria)
admin.site.register(Marca, admMarca)
admin.site.register(Producto, admProducto)
admin.site.register(Carrito, admCarrito)

# Register your models here.
