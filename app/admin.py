from django.contrib import admin
from app.models import Categoria, Producto, Marca, Pedido
from app.models import Categoria, Producto, Marca, ImagenProducto

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
        

class admImagenProducto(admin.TabularInline):
    
    model = ImagenProducto
    
class amdProducto(admin.ModelAdmin):
    list_display=["id_producto", "nom_producto", "precio", "descripcion", "stock", "categoria", "marca"]
    list_editable=["nom_producto", "precio", "descripcion", "stock", "categoria", "marca"]
    inlines = [admImagenProducto]
    class meta:
        model=Producto

class admImagenProducto2(admin.ModelAdmin):
    list_display= ["id_imagen","producto","imagen"]
    list_editable=["producto","imagen"]
    class Meta:
        model=ImagenProducto

class admPedido(admin.ModelAdmin):
    list_display=["producto", "precio", "cantidad", "usuario_id", "estado"]
    list_editable=["estado"]

    class meta:
        model=Pedido

admin.site.register(Categoria, admCategoria)
admin.site.register(Marca, admMarca)
admin.site.register(Producto, amdProducto)
admin.site.register(ImagenProducto, admImagenProducto2)
admin.site.register(Pedido, admPedido)
# Register your models here.
