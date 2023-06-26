from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto,Carrito,Pedido
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from .forms import frmPago

# Create your views here.
def index(request):
    producto=Producto.objects.all()
    context= {
        "producto":producto
    }
    return render(request, 'app/usuario/index_principal.html', context)

def index_admin(request):
    return render(request, 'app/admin/index_admin.html')

def categoria(request):
    producto=Producto.objects.all()
    context= {
        "producto":producto
    }
    return render(request, 'app/usuario/categoria.html', context)

def detalle_producto(request, id):
    producto_det = get_object_or_404(Producto, id_producto = id)
    return render(request, "app/usuario/producto.html", {'producto_det':producto_det})

@login_required
def carrito(request):
    items = Carrito.objects.filter(usuario = request.user)
    cantidad_items = Carrito.objects.filter(usuario = request.user).count()
    total = sum(item.precio * item.cantidad for item in items)
    data = {
        'items':items,
        'total':total,
        'cantidad':cantidad_items
    }
    return render(request, 'app/usuario/carroCompra.html', data)

@login_required
def addCarrito(request, id):
    user_cl = request.user
    producto = get_object_or_404(Producto, id_producto = id)
    carro_cliente = Carrito.objects.filter(usuario = user_cl)
    producto_cliente = carro_cliente.filter(producto = producto.nom_producto)
    if producto_cliente.count() >= 1:
        producto_carro = producto_cliente.get(producto = producto.nom_producto)
        cantidad = producto_carro.cantidad
        producto_carro.cantidad = cantidad + 1
        producto_carro.save()
    else:
        item = Carrito(usuario=user_cl,producto=producto.nom_producto, precio=producto.precio, cantidad=1)
        item.save()
    return redirect(to='categoria')

@login_required
def removeCarrito(request, id):
    item = get_object_or_404(Carrito,id=id)
    item.delete()
    messages.success(request,"Producto eliminado correctamente")  
    return redirect(to="carro")

@login_required
def checkout(request):
    items = Carrito.objects.filter(usuario = request.user)
    total = sum(item.precio * item.cantidad for item in items)
    if request.method == "POST":
        form = frmPago(data=request.POST)
        carrito_filas = Carrito.objects.filter(usuario = request.user)
        for fila in carrito_filas.values():
            Pedido.objects.create(**fila)
        items.delete()
        return redirect(to="index")# Cambiar a "pedidos usuario" cuando este hecho
        
    else:
        form = frmPago()
    context = {
        'items':items,
        'total':total,
        "form":form
    }
    return render(request, 'app/usuario/pago.html', context)