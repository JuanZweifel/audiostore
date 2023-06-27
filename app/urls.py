from django.contrib import admin
from django.urls import include,path
from .views import index, categoria, detalle_producto, index_admin, crear_cuenta, login_view, adminPedido, lista_pedidos
from .views import perfil_usuario, modificar_usuario, removePedido
from .views import index, categoria, detalle_producto, index_admin, carrito, addCarrito, removeCarrito,checkout


urlpatterns = [
    path('', index, name='index'),
    path('categoria', categoria, name='categoria'),
    path('producto/<int:id>/', detalle_producto, name='detalle_producto'),
    path('index_admin', index_admin, name='index_admin'),
    path('login/', login_view, name='loginn'),
    path('accounts/crear_cuenta', crear_cuenta, name='crearcuenta'),
    path('perfil_usuario', perfil_usuario, name='perfil_usuario'),
    path('modificar_usuario/<id>', modificar_usuario, name='modificar_usuario'),
    path('carro', carrito, name='carro'),
    path('addCarrito/<id>/', addCarrito, name='addCarrito'),
    path('removeCarrito/<id>/', removeCarrito, name='removeCarrito'),
    path('checkout', checkout, name='checkout'),
    path('addPedido', addCarrito, name='addPedido'),
    path('adminPedido', adminPedido, name='adminPedido'),
    path('lista_pedidos',lista_pedidos, name='lista_pedidos'),
    path('removePedido/<id>/', removePedido, name='removePedido'),
]