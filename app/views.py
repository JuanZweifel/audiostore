from django.shortcuts import render
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