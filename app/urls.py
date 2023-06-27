from django.contrib import admin
from django.urls import include,path
from .views import modificarproducto, eliminarproducto,productos
from .views import index, categoria, detalle_producto, index_admin, crearproducto, lista_productos
urlpatterns = [
    path('', index, name='index'),
    path('categoria', categoria, name='categoria'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),
    path('index_admin', index_admin, name='index_admin'),
    path('crearproductos', crearproducto, name='crearproductos'),
    path('modificarproducto/<id>',modificarproducto, name="modificarproducto"),
    path('eliminarproducto/<id>',eliminarproducto, name="eliminarproducto"),
    path('productos',productos, name="productos"),
    path('lista_productos/',lista_productos, name='lista_productos'),
    
]