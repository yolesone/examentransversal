from django.shortcuts import get_object_or_404, redirect, render
from .forms import usuarioRegistro,usuarioEdit
from django.contrib.auth import authenticate,login as auth_login
from django.contrib.auth.models import User
from .forms import usuarioRegistro,usuarioEdit
from .models import Producto, Venta, DetalleVenta
from .forms import VentaForm, usuarioAdmin
from django.http import Http404
from rest_framework import viewsets
from .serializers import ProductoSerializer

from carro.carro import Carro
from django.contrib import messages

import requests
# Create your views here.
def home(request):
    print("Estoy en home")
    response = requests.get('https://dog.ceo/api/breeds/image/random/50')
    perros = response.json()

    context={

        'perros':perros,
    }

    return render(request,'core/home.html',context)


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    pass


def tienda(request):
    print("Estoy en tienda")
    productos = Producto.objects.all()
    context={

        'productos':productos
    }
    return render(request,'core/tienda.html',context)

def detail(request, pk):
    producto = Producto.objects.get(idProducto=pk)
    context = {
        "producto": producto
    }
    return render(request, 'core/detalle.html', context)

def carrito(request):
    print('Estoy en carrito')
    context={}
    return render(request,'core/carrito.html',context)

def procesar_venta(request):

    venta = Venta.objects.create(user=request.user)
    carro = Carro(request)
    productos_venta = list()

    for key,value in carro.carro.items():

        producto = Producto.objects.get(idProducto = key)
        nuevoStock = producto.stock - value["cantidad"]
        print(nuevoStock)
        Producto.objects.filter(idProducto= key).update(stock=nuevoStock)
        productos_venta.append(
            DetalleVenta(
                producto_id = producto,
                cantidad=value["cantidad"],
                user = request.user,
                venta_id = venta
            )        
        )

    DetalleVenta.objects.bulk_create(productos_venta)
    carro.vaciar_carro()
    return redirect('mis_pedidos')

def pedidos(request):
    detalleventa = DetalleVenta.objects.all()
    context={"detalleventa":detalleventa
                }
    return render(request,'mantenedor/pedidos.html',context)

def mis_pedidos(request):
    venta = Venta.objects.filter(user= request.user)
    context={"venta":venta}
    return render(request,'core/mis_pedidos.html',context)

def editar_pedido(request, pk):
    mensajes=[]
    errores=[]
    ventas = Venta.objects.all()
    venta =  get_object_or_404(Venta, id=pk)

    if venta:
        form = VentaForm(request.POST or None,
                            request.FILES or None, instance=venta)
        #form = Formalumno(instance=alumno)
        print("estoy en venta")
        if request.method == 'POST':
            print("ingresó al POST")
            #form = Formalumno(request.POST, request.FILES)
           # print("formulario id_persona: " + form.id_persona)
            if form.is_valid():
                print("is valid...")
                venta = form.save()
                venta.save()
                mensajes.append("Bien!, datos grabados...")
                print("Bien!, datos grabados...")
                accion = 'tabla'
                context = {'ventas': ventas, 'mensajes': mensajes,
                           'errores': errores, 'accion': accion}
            else:
                errores.append("Error!, datos no grabados...del EDIT")
                print("Error!, datos no grabados... form="+str(form.errors))
                accion='tabla'
                context = {'ventas': ventas, 'mensajes': mensajes,
                       'errores': errores, 'accion': accion}

            return render(request, 'mantenedor/pedidos.html', context)
        else:
            mensajes.append("Bien!, id existe...")
            print("entró al else form=alumno()...")
            accion = 'form_edit'
            context = {'ventas': ventas, 'mensajes': mensajes,
                       'errores': errores,'form':form, 'accion': accion}
            return render(request, 'mantenedor/pedidos.html', context)

    else:
        print("Error, id_alumno no existe")
        errores.append("Error id no encontrado.")
        accion='tabla'
        context = {'ventas': ventas, 'mensajes': mensajes,
                   'errores': errores, 'accion':accion}
        return render(request, 'core/pedidos.html', context)

def detalle_pedido(request,pk):
    detalleventa = DetalleVenta.objects.filter(venta_id = pk)
    context={"detalleventa":detalleventa,
                "pk":pk}
    print(context)
    return render(request,'core/det_pedido.html',context)

def mantenedor(request):
    print("Estoy en mantenedor")
    context={}
    return render(request,'mantenedor/mantenedor.html',context)

def productosAdd(request):
    print("Estoy en mantenedor (add)")
    context = {}
    if request.method == "POST":
        print("contralador es un post...")
        opcion = request.POST.get("opcion", "")
        print("opcion="+opcion)
        # Listar
        if opcion == "Volver":
            productos = Producto.objects.all()
            context = {'productos': productos}
            return redirect('productos')
        # Agregar
        if opcion == "Agregar":
            idProducto = request.POST["idProducto"]
            nombreProducto = request.POST["nombreProducto"]
            stock = int(request.POST["stock"])
            precio = int(request.POST["precio"])
            activo = int(request.POST["activo"])
            try:
                foto = request.FILES['foto']
            except:
                foto = ""

            if idProducto != "" and nombreProducto != "" and stock != "" and precio != "":
                producto = Producto(idProducto, nombreProducto,
                                    stock, precio, activo, foto)
                producto.save()
                messages.success(request,"Agregado correctamente")

                
            else:
                messages.error(request,"Error, los campos no deben estar vacios")
                context = {
                    'mensaje': "Error, los campos no deben estar vacios"}

            return redirect('productos')
           # Actualizar
        if opcion == "Actualizar":
            idProducto = request.POST["idProducto"]
            nombreProducto = request.POST["nombreProducto"]
            stock = request.POST["stock"]
            precio = request.POST["precio"]
            activo = request.POST["activo"]
            foto = request.FILES['foto']

            if idProducto != "" and nombreProducto != "" and stock != "" and precio != "":
                producto = Producto(idProducto, nombreProducto,
                                    stock, precio, activo, foto)
                producto.save()
                context = {'producto': producto}
                messages.success(request,"Modificado correctamente")
            else:
                messages.error(request,"Error. Los campos no deben estar vacios")
                context = {
                    'mensaje': "Error, los campos no deben estar vacios"}
            return redirect('productos')

    return redirect('productos')


def productos(request):
    productos = Producto.objects.all()
    context={"productos":productos}
    return render(request,'mantenedor/productos.html',context)

def productos_del(request, pk):
    mensajes = []
    errores = []
    productos = Producto.objects.all()
    try:
        producto = Producto.objects.get(idProducto=pk)
        context = {}
        if producto:
            producto.delete()
            messages.success(request,"Eliminado correctamente correctamente")
            mensajes.append("Bien, datos eliminados...")

            context = {'productos': productos,
                       'mensajes': mensajes, 'errores': errores}

            return redirect('productos')

    except:
        print("Error, id no existe")
        errores.append("Error id no encontrado.")
        context = {'productos': productos,
                   'mensajes': mensajes, 'errores': errores}
        return redirect('productos')

def productos_edit(request, pk):

    # try:
    producto = Producto.objects.get(idProducto=pk)

    context = {}
    if producto:
        print("Edit encontró el producto...")

        context = {'producto': producto}

        return render(request, 'mantenedor/productos_edit.html', context)
        messages.success(request,"Modificado correctamente")

    return render(request, 'mantenedor/productos_edit.html', context)

def usuarios(request):
    print("Estoy en mantenedor: usuarios")
    usuarios= User.objects.all()
    context={"usuarios":usuarios}
    return render(request,'mantenedor/usuarios.html',context)

def cargar_formulario_usuario(request):
    context = {}
    mensajes = []
    errores = []
    accion = 'tabla'
    if request.method == 'POST':
        print("Alumno Post")
        form = usuarioRegistro(request.POST or None, request.FILES or None)
        print("Alumno Post 2")
        if form.is_valid():
            print("Alumno Post is_valid")

            alumno = form.save()
            #alumno.save()
            mensajes.append("Bien!, datos grabados...")
            print("Bien!, datos grabados...")
            alumnos=User.objects.all()
            context = {'form':form, 'mensajes': mensajes,'accion': accion,'usuarios':usuarios}
            return render(request,'mantenedor/usuarios.html', context)
            messages.success(request,"Usuario agregado correctamente")
            
        else:
            errores.append( form)
            print("No pasó el is_valid ", form.is_valid())    

    else:
        print("Mostrando formulario alumno...")
        form = usuarioRegistro
        accion = 'form_add'

    context = {'form':form, 'mensajes': mensajes,'accion': accion,'errores':errores}
    return render(request,'mantenedor/usuarios.html', context)
    messages.success(request,"Usuario agregado correctamente")

def cargar_formulario_admin(request):
    context = {}
    mensajes = []
    errores = []
    accion = 'tabla'
    if request.method == 'POST':
        print("Alumno Post")
        form = usuarioAdmin(request.POST or None, request.FILES or None)
        print("Alumno Post 2")
        if form.is_valid():
            print("Alumno Post is_valid")

            alumno = form.save()
            #alumno.save()
            mensajes.append("Bien!, datos grabados...")
            print("Bien!, datos grabados...")
            alumnos=Usuario.objects.all()
            context = {'form':form, 'mensajes': mensajes,'accion': accion,'usuarios':usuarios}
            return render(request,'mantenedor/usuarios.html', context)
            messages.success(request,"Usuario agregado correctamente")
        else:
            errores.append( form)
            print("No pasó el is_valid ", form.is_valid())    

    else:
        print("Mostrando formulario alumno...")
        form = usuarioAdmin
        accion = 'form_add'

    context = {'form':form, 'mensajes': mensajes,'accion': accion,'errores':errores}
    return render(request,'mantenedor/usuarios.html', context)
    messages.success(request,"Usuario agregado correctamente")

def editar_usuario(request, pk):
    mensajes=[]
    errores=[]
    usuarios = User.objects.all()
    usuario =  get_object_or_404(User, id=pk)

    if usuario:
        form = usuarioEdit(request.POST or None,
                            request.FILES or None, instance=usuario)
        #form = Formalumno(instance=alumno)
        print("estoy en alumno true")
        if request.method == 'POST':
            print("ingresó al POST")
            #form = Formalumno(request.POST, request.FILES)
           # print("formulario id_persona: " + form.id_persona)
            if form.is_valid():
                print("is valid...")
                usuario = form.save()
                usuario.save()
                mensajes.append("Bien!, datos grabados...")
                print("Bien!, datos grabados...")
                messages.success(request,"Usuario modificado correctamente")
                accion = 'tabla'
                context = {'usuarios': usuarios, 'mensajes': mensajes,
                           'errores': errores, 'accion': accion}
            else:
                errores.append("Error!, datos no grabados...del EDIT")
                print("Error!, datos no grabados... form="+str(form.errors))
                accion='tabla'
                context = {'usuarios': usuarios, 'mensajes': mensajes,
                       'errores': errores, 'accion': accion}

            return redirect('usuarios')
        else:
            mensajes.append("Bien!, id existe...")
            print("entró al else form=alumno()...")
            accion = 'form_edit'
            context = {'usuarios': usuarios, 'mensajes': mensajes,
                       'errores': errores,'form':form, 'accion': accion}
            return render(request, 'mantenedor/usuarios.html', context)

    else:
        print("Error, id_alumno no existe")
        errores.append("Error id no encontrado.")
        accion='tabla'
        context = {'usuarios': usuarios, 'mensajes': mensajes,
                   'errores': errores, 'accion':accion}
        return render(request, 'core/usuarios.html', context)

def registro(request):
    data ={ 
        'form':usuarioRegistro()
    }

    if request.method == 'POST':
        formulario = usuarioRegistro(data = request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Usuario agregado correctamente")
            user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
            auth_login(request, user)
            return redirect(to='home')
        data["form"] = formulario

    return render(request, 'registration/registro.html',data)