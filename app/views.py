from django.shortcuts import render, get_object_or_404
from .models import Producto

# Create your views here.
def index(request):
    producto=Producto.objects.all()
    context= {
        "producto":producto
    }
    return render(request, 'app/index_principal.html', context)

def categoria(request):
    producto=Producto.objects.all()
    context= {
        "producto":producto
    }
    return render(request, 'app/categoria.html', context)

def detalle_producto(request, id):
    producto_det = get_object_or_404(Producto, id_producto = id)
    return render(request, "app/producto.html", {'producto_det':producto_det})