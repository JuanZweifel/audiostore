from django.contrib import admin
from app.models import Categoria, Producto, Marca

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
        
        
class amdProducto(admin.ModelAdmin):
    list_display=["id_producto", "nom_producto", "precio", "descripcion", "stock", "categoria", "marca"]
    list_editable=["nom_producto", "precio", "descripcion", "stock", "categoria", "marca"]
    class meta:
        model=Producto

admin.site.register(Categoria, admCategoria)
admin.site.register(Marca, admMarca)
admin.site.register(Producto, amdProducto)

# Register your models here.
