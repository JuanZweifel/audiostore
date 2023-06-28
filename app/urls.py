from django.contrib import admin
from django.urls import include,path
from .views import index, categoria, detalle_producto, index_admin, crear_cuenta, login_view, adminPedido, lista_pedidos, updatePedido
from .views import perfil_usuario, modificar_usuario, removePedido
from .views import index, categoria, detalle_producto, index_admin, carrito, addCarrito, removeCarrito,checkout
from .views import clientes_admin, lista_clientes, modificar_cliente, eliminar_cliente


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
    path('updatePedido/<id>/', updatePedido, name='updatePedido'),
    path('clientes_admin', clientes_admin, name= 'clientes_admin'),
    path('lista_clientes/',lista_clientes, name='lista_clientes'),
    path('modificar_cliente/<id>', modificar_cliente, name='modificar_cliente'),
    path('eliminar_cliente/<id>',eliminar_cliente, name='eliminar_cliente' ),
]