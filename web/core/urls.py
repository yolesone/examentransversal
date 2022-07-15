from django.urls import path,include
from django.conf.urls import url
from . import views


from .views import ProductoViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('producto', ProductoViewSet)

urlpatterns = [

    path('',views.home, name='home'),
    path('tienda',views.tienda, name='tienda'),
    path('detalle/<str:pk>', views.detail, name='detalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('procesar_venta/',views.procesar_venta,name='procesar_venta'),

    path("mis_pedidos/",views.mis_pedidos, name='mis_pedidos'),
    path('det_pedido/<int:pk>', views.detalle_pedido, name='det_pedido'),

    path("pedidos", views.pedidos, name='pedidos'),
    path('editar_pedido/<int:pk>', views.editar_pedido, name='editar_pedido'),

    path('mantenedor/',views.mantenedor,name='mantenedor'),
    path('usuarios/',views.usuarios,name='usuarios'),

    path('productos/',views.productos,name='productos'),
    path("productos/productosAdd", views.productosAdd, name='productosAdd'),
    path('productos_edit/<str:pk>', views.productos_edit, name='productos_edit'),
    path('productos_del/<str:pk>', views.productos_del, name='productos_del'),

    path('registro/',views.registro,name='registro'),

    path('cargar_formulario_usuario', views.cargar_formulario_usuario, name='cargar_formulario_usuario'),
    path('cargar_formulario_admin', views.cargar_formulario_admin, name='cargar_formulario_admin'),
    path('editar_usuario/<str:pk>', views.editar_usuario, name='editar_usuario'),

    path('api/', include(router.urls)),    
    
    ]