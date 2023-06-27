import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from .models import Producto, ImagenProducto, Marca, Categoria
from .forms import frmProducto, frmImagen, ImageFormSet
from django.http.response import JsonResponse

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
        
        return redirect(to="index_admin") 
    
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
    #Verificar cuantas imagenes tiene asociada una noticia para poder indicar el numero de formularios extra del formset
    numero_imagenes = ImagenProducto.objects.filter(producto=producto).count()
    numero_imagenes_formset = 3-numero_imagenes
    ImageFormSet = modelformset_factory(ImagenProducto, form=frmImagen, extra=numero_imagenes_formset, can_delete=True, can_delete_extra=True)
    formset = ImageFormSet(queryset=ImagenProducto.objects.filter(producto=producto))


    if request.method == "POST":
        form = frmProducto(request.POST, instance=producto)
        formset = ImageFormSet(request.POST, request.FILES, queryset=ImagenProducto.objects.filter(producto=producto))
        
        if form.is_valid() and formset.is_valid():
            producto = form.save()
            formset.save(commit=False)
            for formm in formset:                
                if  formm.cleaned_data.get('imagen'):
                    imagen_id = formm.instance.id_imagen
                    if imagen_id:
                        # Eliminar la imagen existente
                        try:
                            imagenn = ImagenProducto.objects.get(id_imagen=imagen_id)
                            img = formm.instance.imagen
                            if imagenn.imagen != img:
                                ruta_imagen = imagenn.imagen.url
                                ruta_media = os.path.join(settings.MEDIA_ROOT)
                                nombre = os.path.basename(ruta_imagen)
                                ruta_final = ruta_media + '/Productos/' + nombre
                            
                                if os.path.exists(ruta_final):
                                    os.remove(ruta_final)
                            
                        except ImagenProducto.DoesNotExist:
                            pass 

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
                            
            return redirect('index_admin')

    context = {
        'form': form,
        'formset': formset,
    }
    return render(request, 'app/admin/adminProductoModificar.html', context)


def eliminarproducto(request,id):
    producto=get_object_or_404(Producto,id_producto=id)

    contexto={

        "producto":producto,
    }

    if request.method=="POST":
        img = ImagenProducto.objects.filter(producto=producto)
        
        if img:
            for imagenn in img:
                    ruta_imagen = imagenn.imagen.url
                    ruta_media = os.path.join(settings.MEDIA_ROOT)
                    nombre = os.path.basename(ruta_imagen)
                    ruta_final = ruta_media + '/Productos/' + nombre
                
                    if os.path.exists(ruta_final):
                        os.remove(ruta_final)
        producto.delete()
        return redirect(to="index_admin")


    return render(request,"app/admin/adminProductoEliminar.html",contexto)


def productos(request):

    
    return render(request,"app/admin/adminProducto.html")

def lista_productos(_request):
    productos = list(Producto.objects.values())

    for producto in productos:
        idmarca= producto['marca_id']
        idcategoria= producto['categoria_id']
        
        producto['marca_id']=Marca.objects.get(id_marca=idmarca).nom_marca
        producto['categoria_id']=Categoria.objects.get(id_cat=idcategoria).nom_cat
    
    data={'productos':productos}
    
    return JsonResponse(data)
