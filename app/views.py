from django.contrib.auth.decorators import login_required,permission_required
from django.http.response import JsonResponse
from .models import Producto, Cliente
from .models import Producto,Carrito,Pedido
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import LoginForm, frmCrearCuenta, frmPerfilCliente, frmModifDatosCliente
from .forms import frmPago
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from .models import Producto, ImagenProducto, Marca, Categoria
from .forms import frmProducto, frmImagen, ImageFormSet
from django.http.response import JsonResponse

# Create your views here.
def index(request):
    return render(request, 'app/usuario/index_principal.html')

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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,"Identificado correctamente")
                if user.is_staff:
                    return redirect(to="index_admin")  # Redirige al apartado de administración
                else:
                    return redirect(to="index")  # Redirige a la página de inicio de usuario normal
    else:
        form = LoginForm()
    
    return render(request, 'registration/loginn.html', {'form': form})

def crear_cuenta(request):
    formext=frmCrearCuenta(request.POST or None)
    formnormal=frmPerfilCliente(request.POST or None)

    contexto={
        "form":formext,
        "fuser":formnormal
        
    }

    if request.method=="POST":
        if formnormal.is_valid() and formext.is_valid():
            formext.save()
            datoext=formext.cleaned_data
            usr=User.objects.get(username=datoext.get("username"))
            u=Cliente()
            datos=formnormal.cleaned_data
            u.run=datos.get("run") 
            u.primer_nombre=datos.get("primer_nombre")
            u.segundo_nombre=datos.get("segundo_nombre")
            u.apellido_paterno=datos.get("apellido_paterno")
            u.apellido_materno=datos.get("apellido_materno")
            u.correo=datos.get("correo")
            u.usuario=usr
            u.save()
            messages.success(request,"Cuenta creada correctamente")
            return redirect(to="index")
            
    return render(request,"registration/crearcuenta.html",contexto)

@login_required
def perfil_usuario(request):
    usuario=request.user
    cliente=Cliente.objects.get(usuario=usuario)
    contexto={
        "cliente":cliente
    }
    
    
    return render(request, 'app/usuario/perfil_usuario.html', contexto)

def modificar_usuario(request,id):
    modificar=get_object_or_404(Cliente,run=id)
    
    form = frmModifDatosCliente(instance=modificar)
    contexto={
        "form":form,
        "modificar":modificar
    }
    
    if request.method=="POST":
        
        form=frmModifDatosCliente(data=request.POST,instance=modificar)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Cuenta modificada correctamente")
            return redirect(to="index")

    return render(request,"app/usuario/modificar_usuario.html",contexto)

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

@login_required
def adminPedido(request):
    return render(request, 'app/admin/adminPedido.html')

@login_required
def lista_pedidos(info):
    pedidos = list(Pedido.objects.values())
    data={'pedidos':pedidos}
    return JsonResponse(data)

@login_required
def removePedido(request, id):
    item = get_object_or_404(Pedido,id=id)
    item.delete()
    messages.success(request,"Producto eliminado correctamente")  
    return redirect(to="adminPedido")