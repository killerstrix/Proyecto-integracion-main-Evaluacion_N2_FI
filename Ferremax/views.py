from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import marca, categoria, proveedor, producto, cargo, empleado, usuario
from .apiMonedas import dolar, euro
import requests
import json
from django.core.mail import send_mail

from django.conf import settings
from django.http import JsonResponse
from transbank.webpay.webpay_plus.transaction import (
    Transaction,
    WebpayOptions,
    IntegrationCommerceCodes,
    IntegrationApiKeys,
)
from transbank.common.integration_type import IntegrationType

# Create your views here.


def index(request):
    return render(request, "core/index.html")


def Nosotros(request):
    return render(request, "core/Nosotros.html")


def Contacto(request):
    return render(request, "core/Contacto.html")


def crud_cuentas(request):
    if request.method == "POST":
        nombre_empleado = request.POST["nombre_empleado"]
        nombre_completo = request.POST["nombre_completo"]
        correo = request.POST["correo_empleado"]
        edad = request.POST["edad_empleado"]
        contraseña = request.POST["contraseña_empleado"]
        IdCar = request.POST["cargo"]

        objCar = cargo.objects.get(idCargo=IdCar)

        Emp = empleado.objects.create(
            nombreEmpleado=nombre_empleado,
            nombreCompleto=nombre_completo,
            correo=correo,
            edad=edad,
            contraseña=contraseña,
            cargo=objCar,
        )

        Emp.save()
        return redirect("crud_cuentas")

    else:
        Car = cargo.objects.all()
        Empleados = empleado.objects.all()

        context = {"Cargo": Car, "cuenta": Empleados}
        return render(request, "core/crud_cuentas.html", context)


def crud_productos(request):
    if request.method != "POST":
        mar = marca.objects.all()
        cat = categoria.objects.all()
        pro = proveedor.objects.all()
        produ = producto.objects.all()

        context = {"marca": mar, "categoria": cat, "proveedor": pro, "productos": produ}
        return render(request, "core/crud_productos.html", context)

    else:
        nombre_producto = request.POST["txtNombre_Producto"]
        sotck_producto = request.POST["txtstock_Producto"]
        descripcion_producto = request.POST["txtdescripcion_Producto"]
        precio_producto = request.POST["txtPrecio_Producto"]
        imagen_producto = request.FILES["imagen_producto"]
        id_marca = request.POST["marca"]
        id_categoria = request.POST["categoria"]
        id_proveedor = request.POST["proveedor"]

        objMarca = marca.objects.get(idMarca=id_marca)
        objCategoria = categoria.objects.get(idCategoria=id_categoria)
        objProveedor = proveedor.objects.get(idProveedor=id_proveedor)

        cli = producto.objects.create(
            nombreProducto=nombre_producto,
            stockProducto=sotck_producto,
            descripcionProducto=descripcion_producto,
            precioProducto=precio_producto,
            imagenProducto=imagen_producto,
            categoria=objCategoria,
            marca=objMarca,
            proveedor=objProveedor,
        )
        cli.save()

        context = {"mensaje": "Exito"}
        return render(request, "core/resultado.html", context)


def resultado(request):
    context = {}
    return render(request, "core/resultado.html", context)


def pedido(request):
    valorDolar = dolar()
    valorEuro = euro()
    context = {"dolar": valorDolar, "euro": valorEuro}
    return render(request, "core/pedido.html", context)


def Login(request):
    if request.method == "POST":
        nombre_usuario = request.POST["nombreUsuario"]
        contraseña = request.POST["contraseña"]

        if nombre_usuario and contraseña:
            try:
                usu = usuario.objects.get(
                    nombreUsuario=nombre_usuario, contraseña=contraseña
                )
            except usuario.DoesNotExist:
                usu = None

            try:
                emp = empleado.objects.get(
                    nombreEmpleado=nombre_usuario, contraseña=contraseña
                )
            except empleado.DoesNotExist:
                emp = None

            if usu is not None:
                request.session["nombreUsuario"] = nombre_usuario
                return render(request, "core/index.html")
            elif emp is not None:
                request.session["nombreEmpleado"] = nombre_usuario
                context = {}
                return render(request, "core/IndexEmpleados.html", context)

        return render(
            request,
            "core/Login.html",
        )

    return render(
        request,
        "core/Login.html",
    )


def registro(request):
    if request.method == "POST":
        nombre_usuario = request.POST["nombreUsuario"]
        nombre_completo = request.POST["nombreCompleto"]
        correo = request.POST["correo"]
        contraseña1 = request.POST["contraseña1"]
        contraseña2 = request.POST["contraseña2"]

        if contraseña1 == contraseña2:
            usu = usuario.objects.create(
                nombreUsuario=nombre_usuario,
                nombreCompleto=nombre_completo,
                correo=correo,
                contraseña=contraseña1,
            )
            usu.save()
            send_mail(
                "Confirmación de registro",
                "Gracias por registrarte en Ferremax.",
                settings.EMAIL_HOST_USER,
                [usu.correo],
                fail_silently=False,
            )
            return render(request, "core/Login.html")

        else:
            return render(request, "core/registro.html")

    context = {}
    return render(request, "core/registro.html", context)


def pago(request):
    buy_order = request.POST["ordenCompra"]
    session_id = request.POST["idSesion"]
    amount = request.POST["monto"]
    return_url = "http://127.0.0.1:8000/retorno_pago"

    transaction = Transaction(
        WebpayOptions(
            IntegrationCommerceCodes.WEBPAY_PLUS,
            IntegrationApiKeys.WEBPAY,
            IntegrationType.TEST,
        )
    )

    response = transaction.create(buy_order, session_id, amount, return_url)
    token = response["token"]
    url = response["url"]

    return render(request, "core/pago.html", {"url": url, "token": token})


def retorno_pago(request):
    token = request.GET.get("token_ws")

    transaction = Transaction(
        WebpayOptions(
            IntegrationCommerceCodes.WEBPAY_PLUS,
            IntegrationApiKeys.WEBPAY,
            IntegrationType.TEST,
        )
    )

    response = transaction.commit(token)

    status = response["status"]
    amount = response["amount"]
    buy_order = response["buy_order"]

    context = {
        "status": status,
        "amount": amount,
        "buy_order": buy_order,
    }

    return render(request, "core/retorno_pago.html", context)


def productos(request):
    url = "http://localhost:8000/api/v1/productos"

    try:
        response = requests.get(url)
        response.raise_for_status()
        datos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al hacer la solicitud a la API: {e}")
        datos = None

    context = {"productos": datos}

    return render(request, "core/productos.html", context)


def eliminarProducto(request, pk):
    prod = producto.objects.get(idProducto=pk)
    prod.delete()

    return redirect("crud_productos")


def edicion_producto(request, pk):
    if request.method != "POST":

        prod = producto.objects.get(idProducto=pk)
        mar = marca.objects.all()
        cat = categoria.objects.all()
        prov = proveedor.objects.all()
        context = {"producto": prod, "marca": mar, "categoria": cat, "proveedor": prov}
        return render(request, "core/edicion_producto.html", context)
    else:
        id_producto = request.POST["id_Producto"]
        nombre_producto = request.POST["txtNombre_Producto"]
        sotck_producto = request.POST["txtstock_Producto"]
        descripcion_producto = request.POST["txtdescripcion_Producto"]
        precio_producto = request.POST["txtPrecio_Producto"]
        id_marca = request.POST["marca"]
        id_categoria = request.POST["categoria"]
        id_proveedor = request.POST["proveedor"]

        objMarca = marca.objects.get(idMarca=id_marca)
        objCategoria = categoria.objects.get(idCategoria=id_categoria)
        objProveedor = proveedor.objects.get(idProveedor=id_proveedor)

        prod = producto.objects.get(idProducto=id_producto)

        prod.nombreProducto = nombre_producto
        prod.stockProducto = sotck_producto
        prod.descripcionProducto = descripcion_producto
        prod.precioProducto = precio_producto
        if "imagen_producto" in request.FILES:
            prod.imagenProducto = request.FILES["imagen_producto"]
        prod.categoria = objCategoria
        prod.marca = objMarca
        prod.proveedor = objProveedor

        prod.save()

        return redirect("crud_productos")


def IndexEmpleados(request):
    return render(request, "core/IndexEmpleados.html")


def Logout(request):
    del request.session["nombreUsuario"]
    return redirect("index")


def EliminarCuenta(request, pk):
    Emp = empleado.objects.get(idEmpleado=pk)
    Emp.delete()

    return redirect("crud_cuentas")
