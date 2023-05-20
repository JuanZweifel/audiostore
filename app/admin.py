from django.contrib import admin
from app.models import Categoria
from app.models import Marca

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

admin.site.register(Categoria, admCategoria)
admin.site.register(Marca, admMarca)