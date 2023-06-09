from django.contrib.auth.decorators import login_required,permission_required
from django.http.response import JsonResponse
from .models import Producto, Cliente
from .models import Producto,Carrito,Pedido, DetallePedido
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import LoginForm, frmCrearCuenta, frmPerfilCliente, frmModifDatosCliente
from .forms import frmPago
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from .models import Producto, ImagenProducto, Marca, Categoria
from .forms import frmProducto, frmImagen, ImageFormSet, frmCategoria, frmMarca, BusquedaForm
from django.http.response import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

# Create your views here.
def index(request):
    productos = Producto.objects.all()
    formbusqueda = BusquedaForm(request.GET)
    for producto in productos:
        img = ImagenProducto.objects.filter(producto=producto)
        
        if img.exists():
            producto.imagen=img[0]
        
    context= {
        'formbusqueda':formbusqueda,
        'productos':productos
    }
    
    return render(request, 'app/usuario/index_principal.html', context)

@staff_member_required(login_url="loginn")
def index_admin(request):
    return render(request, 'app/admin/index_admin.html')

def categoria(request):
    formbusqueda = BusquedaForm(request.GET)
    productos = Producto.objects.all()

    if formbusqueda.is_valid():
        busqueda = formbusqueda.cleaned_data.get('busqueda')
        categoria_id = formbusqueda.cleaned_data.get('categoria')
        marca_id = formbusqueda.cleaned_data.get('marca')
        
        
        if busqueda:
            productos = productos.filter(nom_producto__icontains=busqueda)

        if categoria_id:
            productos = productos.filter(categoria_id=categoria_id)
    
        if marca_id:
            productos = productos.filter(marca_id=marca_id)
    
    
    for producto in productos:
        img = ImagenProducto.objects.filter(producto=producto)
        
        if img.exists():
            producto.imagen=img[0]
        
    context= {
        'formbusqueda':formbusqueda,
        'productos':productos
    }
    
    return render(request, 'app/usuario/categoria.html', context)

def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id_producto = id)
    formbusqueda = BusquedaForm(request.GET)
    
    imagenes = ImagenProducto.objects.filter(producto=producto)
    imagen1 = None
    imagen2 = None
    imagen3 = None

    if imagenes.exists():
        imagen1 = imagenes[0]
        if len(imagenes) >= 2:
            imagen2 = imagenes[1]
        if len(imagenes) >= 3:
            imagen3 = imagenes[2]
    
    
    context= {
        'formbusqueda':formbusqueda,
        'producto':producto,
        'imagen1':imagen1,
        'imagen2':imagen2,
        'imagen3':imagen3
    }

    return render(request, "app/usuario/producto.html",context)

@staff_member_required(login_url="loginn")
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


@staff_member_required(login_url="loginn")
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
                            
            return redirect(to="productos")

    context = {
        'form': form,
        'formset': formset,
        'producto':producto,
    }
    return render(request, 'app/admin/adminProductoModificar.html', context)


@staff_member_required(login_url="loginn")
def eliminarproducto(request,id):
    producto=get_object_or_404(Producto,id_producto=id)


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
    
    messages.success(request,"Producto eliminado correctamente")
    return redirect(to="productos")

@staff_member_required(login_url="loginn")
def productos(request):

    
    return render(request,"app/admin/adminProducto.html")

@staff_member_required(login_url="loginn")
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
    formbusqueda = BusquedaForm(request.GET)
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
    
    
    
    return render(request, 'registration/loginn.html', {'form': form, 'formbusqueda':formbusqueda})

def crear_cuenta(request):
    formext=frmCrearCuenta(request.POST or None)
    formnormal=frmPerfilCliente(request.POST or None)
    formbusqueda = BusquedaForm(request.GET)

    contexto={
        'formbusqueda':formbusqueda,
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
    formbusqueda = BusquedaForm(request.GET)
    usuario=request.user
    cliente=Cliente.objects.get(usuario=usuario)
    contexto={
        'formbusqueda':formbusqueda,
        "cliente":cliente
    }
    
    
    return render(request, 'app/usuario/perfil_usuario.html', contexto)

@login_required
def modificar_usuario(request,id):
    modificar=get_object_or_404(Cliente,run=id)
    formbusqueda = BusquedaForm(request.GET)
    
    form = frmModifDatosCliente(data=request.POST or None, instance=modificar)
    contexto={
        'formbusqueda':formbusqueda,
        "form":form,
        "modificar":modificar
    }
    
    if request.method=="POST":
        
        if form.is_valid():
            form.save()
            messages.success(request,"Cuenta modificada correctamente")
            return redirect(to="perfil_usuario")

    return render(request,"app/usuario/modificar_usuario.html",contexto)

@login_required(login_url="loginn")
def carrito(request):
    items = Carrito.objects.filter(usuario = request.user)
    cantidad_items = Carrito.objects.filter(usuario = request.user).count()
    total = sum(item.precio * item.cantidad for item in items)
    formbusqueda = BusquedaForm(request.GET)
    for producto in items:
        imagen = ImagenProducto.objects.filter(producto=producto.id_producto)
        
        if imagen.exists():
            producto.img=imagen[0]

    data = {
        'formbusqueda':formbusqueda,
        'items':items,
        'total':total,
        'cantidad':cantidad_items
    }

    return render(request, 'app/usuario/carroCompra.html', data)

@login_required(login_url="loginn")
def addCarrito(request, id, cantidad_pag):
    user_cl = request.user
    producto = get_object_or_404(Producto, id_producto = id)
    carro_cliente = Carrito.objects.filter(usuario = user_cl)
    producto_cliente = carro_cliente.filter(id_producto = producto.id_producto)
    if producto.stock > 0:
        if producto_cliente.count() >= 1:
            producto_carro = producto_cliente.get(id_producto = producto.id_producto)
            cantidad = producto_carro.cantidad
            producto_carro.cantidad = cantidad + cantidad_pag
            producto_carro.save()
            messages.success(request,"Se ha sumado el producto a su carro")
        else:
            item = Carrito(usuario=user_cl,id_producto=producto.id_producto, producto=producto.nom_producto, precio=producto.precio, cantidad=cantidad_pag)
            item.save()
            messages.error(request,"Producto añadido al carro correctamente")
    else:
        messages.success(request,"No hay stock del producto")
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
        #Creacion de la instancia en Pedido
        pedido_usu = Pedido(usuario=request.user)
        pedido_usu.save()
        #Rellenado del DetallePedido con la intancia Pedido
        for fila in carrito_filas:
            detalle_pedido = DetallePedido(pedido=pedido_usu,id_producto=fila.id_producto, producto=fila.producto, precio=fila.precio, cantidad=fila.cantidad)
            detalle_pedido.save()
            producto_carro = fila.id_producto
            producto = Producto.objects.get(id_producto=producto_carro)
            cantidad = producto.stock
            producto.stock = cantidad - fila.cantidad
            producto.save()
        
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

@staff_member_required(login_url="loginn")
def adminPedido(request):
    return render(request, 'app/admin/adminPedido.html')

@staff_member_required(login_url="loginn")
def adminPedidoDetalle(request, id):
    items = DetallePedido.objects.filter(pedido=id)
    total = 0
    for item in items:
        suma = item.cantidad * item.precio
        total = total + suma

    context = {
        "items": items,
        "total": total
    }
    return render(request, 'app/admin/adminPedidoDetalle.html', context)

@login_required(login_url="loginn")
def pedidoDetalle(request, id):
    formbusqueda = BusquedaForm(request.GET)
    items = DetallePedido.objects.filter(pedido=id)
    total = 0
    for item in items:
        suma = item.cantidad * item.precio
        total = total + suma

    context = {
        'formbusqueda':formbusqueda,
        "items": items,
        "total": total
    }
    return render(request, 'app/usuario/pedidoDetalle.html', context)

@staff_member_required(login_url="loginn")
def lista_pedidos(info):
    pedidos = list(Pedido.objects.values())
    for pedido in pedidos:
        idusuario = pedido['usuario_id']
        pedido['usuario_id'] = User.objects.get(id=idusuario).username
    data={'pedidos':pedidos}
    return JsonResponse(data)

@login_required
def usuarioPedido(request):
    formbusqueda = BusquedaForm(request.GET)
    context={
        'formbusqueda':formbusqueda
    }
    
    return render(request, 'app/usuario/pedido_usuario.html',context)

@login_required
def lista_pedidos_usuario(request):
    pedidos = list(Pedido.objects.filter(usuario_id = request.user.id).values())
    for pedido in pedidos:
        idusuario = pedido['usuario_id']
        pedido['usuario_id'] = User.objects.get(id=idusuario).username
    data={'pedidos':pedidos}
    return JsonResponse(data)

@staff_member_required(login_url="loginn")
def removePedido(request, id):
    item = get_object_or_404(Pedido,id=id)
    detalles_filas = DetallePedido.objects.filter(pedido_id = id)

    for fila in detalles_filas:
        producto = Producto.objects.get(id_producto=fila.id_producto)
        cantidad = producto.stock
        producto.stock = cantidad + fila.cantidad
        producto.save()
    item.delete()
    messages.success(request,"Pedido eliminado correctamente")  
    return redirect(to="adminPedido")

@login_required(login_url="loginn")
def removePedidoUser(request, id):
    item = get_object_or_404(Pedido,id=id)
    detalles_filas = DetallePedido.objects.filter(pedido_id = id)

    for fila in detalles_filas:
        producto = Producto.objects.get(id_producto=fila.id_producto)
        cantidad = producto.stock
        producto.stock = cantidad + fila.cantidad
        producto.save()
    item.delete()
    messages.success(request,"Pedido eliminado correctamente")  
    return redirect(to="usuarioPedido")

@staff_member_required(login_url="loginn")
def updatePedido(request, id):
    item = get_object_or_404(Pedido,id=id)
    if item.estado == "No Retirado":
        item.estado = "Retirado"
        item.save(update_fields=["estado"])
    else:
        item.estado = "No Retirado"
        item.save(update_fields=["estado"])
    messages.success(request,"Estado cambiado correctamente")  
    return redirect(to="adminPedido")

@staff_member_required(login_url="loginn")
def clientes_admin(request):
    
    
    return render(request, "app/admin/clientes_admin.html")

@staff_member_required(login_url="loginn")
def lista_clientes(_request):
    clientes = list(Cliente.objects.values())
    data={'clientes':clientes}
    return JsonResponse(data)

@staff_member_required(login_url="loginn")
def modificar_cliente(request,id):
    modificar=get_object_or_404(Cliente,run=id)
    
    form = frmModifDatosCliente(data=request.POST or None, instance=modificar)
    contexto={
        "form":form,
        "modificar":modificar
    }
    
    if request.method=="POST":
        
        if form.is_valid():
            form.save()
            messages.success(request,"Cuenta modificada correctamente")
            return redirect(to="clientes_admin")

    return render(request,"app/admin/modificar_cliente.html",contexto)

@staff_member_required(login_url="loginn")
def eliminar_cliente(request,id):
    cliente=get_object_or_404(Cliente,run=id)
    id = cliente.usuario_id
    usuario=User.objects.get(id=id)
    contexto={

        "cliente":cliente
    }

    if request.method=="POST":
        usuario.delete()
        messages.success(request,"Cliente eliminado correctamente")
        return redirect(to="clientes_admin")

    
    return render(request,"app/admin/eliminar_cliente.html",contexto)

@staff_member_required(login_url="loginn")
def categoriaproducto(request):
    if request.method=="POST":
        form = frmCategoria(request.POST)
        
        if form.is_valid():
            form.save()
            
        return redirect(to="categorias") 
    
    else:
        form = frmCategoria()

    context={
        "form":form,

    }
    
    
    return render(request, "app/admin/adminCrearCategoria.html", context)


@staff_member_required(login_url="loginn")
def lista_categorias(_request):
    categorias = list(Categoria.objects.values())
    
    data={'categorias':categorias}
    
    return JsonResponse(data)


@staff_member_required(login_url="loginn")
def categorias(request):

    
    return render(request,"app/admin/adminCategoria.html")


@staff_member_required(login_url="loginn")
def modificarcategoria(request,id):
    categoria=get_object_or_404(Categoria,id_cat=id)
    form = frmCategoria(instance=categoria)
    contexto={
        "form":form,
        "categoria":categoria
    }
    if request.method=="POST":
        form=frmCategoria(data=request.POST,instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request,"Categoria modificada correctamente")  
            return redirect(to="categorias")
    return render(request,"app/admin/adminModificarCategoria.html",contexto)



@staff_member_required(login_url="loginn")
def removeCategoria(request, id):
    item = get_object_or_404(Categoria,id_cat=id)
    messages.success(request,"No se pudo eliminar la categoria")
    
    if not Producto.objects.filter(categoria=item):
        item.delete()
        messages.success(request,"Categoria eliminada correctamente") 
    else:
        messages.success(request,"No se pudo eliminar la categoria") 
    
    return redirect(to="categorias")



@staff_member_required(login_url="loginn")
def lista_marcas(_request):
    marcas = list(Marca.objects.values())
    
    data={'marcas':marcas}
    
    return JsonResponse(data)


@staff_member_required(login_url="loginn")
def marcas(request):

    
    return render(request,"app/admin/adminMarca.html")


@staff_member_required(login_url="loginn")
def crearmarca(request):
    if request.method=="POST":
        form = frmMarca(request.POST)
        
        if form.is_valid():
            form.save()
            
        return redirect(to="marcas") 
    
    else:
        form = frmMarca()

    context={
        "form":form,

    }
    
    return render(request, "app/admin/adminCrearMarca.html", context)

@staff_member_required(login_url="loginn")
def modificarmarca(request,id):
    marca=get_object_or_404(Marca,id_marca=id)
    form = frmMarca(instance=marca)
    contexto={
        "form":form,
        "marca":marca
    }
    if request.method=="POST":
        form=frmMarca(data=request.POST,instance=marca)
        if form.is_valid():
            form.save()
            messages.success(request,"Marca modificada correctamente")  
            return redirect(to="marcas")
    return render(request,"app/admin/adminModificarMarca.html",contexto)



@staff_member_required(login_url="loginn")
def removeMarca(request, id):
    item = get_object_or_404(Marca,id_marca=id)
    
    if not Producto.objects.filter(marca=item):
        item.delete()
        messages.success(request,"Marca eliminada correctamente") 
    else:
        messages.success(request,"No se pudo eliminar la marca") 
    
    return redirect(to="marcas")

@staff_member_required(login_url="loginn")
def removeCliente(request, id):
    cliente=get_object_or_404(Cliente,run=id)
    id = cliente.usuario_id
    usuario=User.objects.get(id=id)

    
    if not Pedido.objects.filter(usuario_id=id):
        usuario.delete()
        messages.success(request,"Cliente eliminado correctamente") 
    else:
        messages.success(request,"No se puede eliminar al cliente") 
    
    return redirect(to="clientes_admin")

@login_required
def change_password(request):
    formbusqueda = BusquedaForm(request.GET)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Su contraseña a sido cambiada con exito!')
            return redirect('logout')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form, 'formbusqueda':formbusqueda})