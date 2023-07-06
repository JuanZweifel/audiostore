from django.contrib import admin
from django.urls import include,path
from .views import index, categoria, detalle_producto, index_admin, crear_cuenta, login_view, adminPedido, lista_pedidos
from .views import perfil_usuario, modificar_usuario, removePedido, categorias, modificarcategoria, removeCategoria
from .views import index, categoria, detalle_producto, index_admin, carrito, addCarrito, removeCarrito,checkout
from .views import clientes_admin, lista_clientes, modificar_cliente, eliminar_cliente, categoriaproducto, lista_categorias
from .views import lista_marcas, marcas, crearmarca, modificarmarca,removeMarca
from .views import index, categoria, detalle_producto, index_admin, crear_cuenta, login_view, adminPedido, lista_pedidos, updatePedido
from .views import perfil_usuario, modificar_usuario, removePedido, lista_pedidos_usuario
from .views import index, categoria, detalle_producto, index_admin, carrito, addCarrito, removeCarrito, checkout, usuarioPedido
from .views import clientes_admin, lista_clientes, modificar_cliente, eliminar_cliente, adminPedidoDetalle, pedidoDetalle, removePedidoUser


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
    path('lista_categorias/',lista_categorias, name='lista_categorias'),
    path('crearcategoria',categoriaproducto, name="crearcategoria"),
    path('modificarcategoria/<id>',modificarcategoria, name="modificarcategoria"),
    path('categorias',categorias, name="categorias"),
    path('removeCategoria/<id>/', removeCategoria, name='removeCategoria'),
    path('lista_marcas/',lista_marcas, name='lista_marcas'),
    path('marcas',marcas, name="marcas"),
    path('crearmarca',crearmarca, name="crearmarca"),
    path('modificarmarca/<id>',modificarmarca, name="modificarmarca"),
    path('removeMarca/<id>/', removeMarca, name='removeMarca'),
    
    
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
    path('usuarioPedido', usuarioPedido, name='usuarioPedido'),
    path('lista_pedidos',lista_pedidos, name='lista_pedidos'),
    path('lista_pedidos_usuario',lista_pedidos_usuario, name='lista_pedidos_usuario'),
    path('removePedido/<id>/', removePedido, name='removePedido'),
    path('removePedidoUser/<id>/', removePedidoUser, name='removePedidoUser'),
    path('updatePedido/<id>/', updatePedido, name='updatePedido'),
    path('clientes_admin', clientes_admin, name= 'clientes_admin'),
    path('lista_clientes/',lista_clientes, name='lista_clientes'),
    path('modificar_cliente/<id>', modificar_cliente, name='modificar_cliente'),
    path('eliminar_cliente/<id>',eliminar_cliente, name='eliminar_cliente' ),
    path('adminPedidoDetalle/<id>', adminPedidoDetalle, name='adminPedidoDetalle'),
    path('pedidoDetalle/<id>', pedidoDetalle, name='pedidoDetalle'),
]