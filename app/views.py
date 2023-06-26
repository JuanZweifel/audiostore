import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from .models import Producto, ImagenProducto
from .forms import frmProducto, frmImagen, ImageFormSet

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

def crearproducto(request):
    if request.method=="POST":
        form = frmProducto(request.POST)
        formset = ImageFormSet(request.POST, request.FILES)
        
        
        if form.is_valid() and formset.is_valid():
            producto= form.save()
            
            for frmset in formset:
                if  frmset.cleaned_data.get('imagen'):
                    imagen = frmset.save(commit=False)
                    imagen.producto = producto
                    imagen.save()
        
        return redirect(to="index") 
    
    else:
        form = frmProducto()
        formset = formset_factory(frmImagen, extra=3, can_delete=True, can_delete_extra=True)
        
    context={
        "form":form,
        "formset":formset
    }
    return render(request, 'app/admin/adminProductoAnadir.html', context)


def modificarproducto(request, id):
    producto = get_object_or_404(Producto,id_producto=id)
    form = frmProducto(instance=producto)
    ImageFormSet = modelformset_factory(ImagenProducto, form=frmImagen, extra=3, can_delete=True, can_delete_extra=True)
    formset = ImageFormSet(queryset=ImagenProducto.objects.filter(producto=producto))

    if request.method == "POST":
        form = frmProducto(request.POST, instance=producto)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ImagenProducto.objects.filter(producto=producto))
        
        
        if form.is_valid() and formset.is_valid():
            producto = form.save()
            
            for formm in formset:                
                if  formm.cleaned_data.get('imagen'):
                    elemento_id  = formm.cleaned_data['id_imagen']
                    if elemento_id:
                        # Eliminar el elemento
                        imagenn = ImagenProducto.objects.get(imagen=elemento_id)
                        if imagenn:
                            ruta_imagen = imagenn.imagen.url
                            ruta_media = os.path.join(settings.MEDIA_ROOT)
                            nombre = os.path.basename(ruta_imagen)
                            ruta_final = ruta_media + '/Productos/' + nombre
                        
                            if os.path.exists(ruta_final):
                                os.remove(ruta_final)
                    #asdsa
                    imagen = formm.save(commit=False)
                    imagen.producto = producto
                    imagen.save()
                
                if formm.cleaned_data.get('DELETE',True) and  formm.cleaned_data.get('imagen',False): 
                    elemento_id  = formm.cleaned_data['id_imagen']
                    if elemento_id:
                        # Eliminar el elemento
                        imagenn = ImagenProducto.objects.get(imagen=elemento_id)
                        ruta_imagen = imagenn.imagen.url
                        ruta_media = os.path.join(settings.MEDIA_ROOT)
                        nombre = os.path.basename(ruta_imagen)
                        ruta_final = ruta_media + '/Productos/' + nombre
                        imagenn.delete()
                        
                        if os.path.exists(ruta_final):
                            os.remove(ruta_final)
                            
            return redirect('index')

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'app/admin/adminProductoModificar.html', context)