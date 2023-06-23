from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto,Carrito

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

def carrito(request):
    items = Carrito.objects.all()
    total = sum(item.precio * item.cantidad for item in items)
    data = {
        'items' : items,
        'total' : total
    }
    return render(request, 'app/usuario/carroCompra.html', data)

def addCarrito(request, id):
    producto = get_object_or_404(Producto, id_producto = id)
    item = Carrito(producto=producto.nom_producto, precio=producto.precio, cantidad=1)
    item.save()
    return redirect(to='categoria')