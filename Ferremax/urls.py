from django.urls import path, include
from rest_framework import routers
from .api import ProductoListView, ProductoDetailView, ProductoUpdateView

from .views import (
    index,
    Nosotros,
    Contacto,
    crud_cuentas,
    crud_productos,
    resultado,
    pedido,
    pago,
    retorno_pago,
    productos,
    Login,
    registro,
    eliminarProducto,
    edicion_producto,
    IndexEmpleados,
    Logout,
    EliminarCuenta
)

""" router = routers.DefaultRouter()
router.register('api/v1/productos', ProductoListView, 'productos') """

urlpatterns = [
    path("", index, name="index"),
    path("Nosotros", Nosotros, name="Nosotros"),
    path("Contacto", Contacto, name="Contacto"),
    path("crud_cuentas", crud_cuentas, name="crud_cuentas"),
    path("crud_productos", crud_productos, name="crud_productos"),
    path("resultado", resultado, name="resultado"),
    path("pedido", pedido, name="pedido"),
    path("pago", pago, name="pago"),
    path("retorno_pago", retorno_pago, name="retorno_pago"),
    path("productos", productos, name="productos"),
    path("Login", Login, name="Login"),
    path("registro", registro, name="registro"),
    path("edicion_producto/<str:pk>", edicion_producto, name="edicion_producto"),
    path("eliminarProducto/<str:pk>", eliminarProducto, name="eliminarProducto"),
    path("IndexEmpleados", IndexEmpleados, name="IndexEmpleados"),
    path("Logout", Logout, name="Logout"),
    path("EliminarCuenta/<str:pk>", EliminarCuenta, name="EliminarCuenta"),
    path('api/v1/productos/', ProductoListView.as_view(), name='apiProductos'),
    path('api/v1/productos/<int:pk>/', ProductoDetailView.as_view(), name='apiProductosID'),
    path('api/v1/productos/<int:pk>/update/', ProductoUpdateView.as_view(), name='apiProductosUpdate'),
]
