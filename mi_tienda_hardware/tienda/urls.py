from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, CarroViewSet, OrdenViewSet, RegistroClienteView

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categorias')
router.register(r'productos', ProductoViewSet, basename='productos')
router.register(r'carro', CarroViewSet, basename='carro')
router.register(r'ordenes', OrdenViewSet, basename='ordenes')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/registro/', RegistroClienteView.as_view(), name='registro_cliente'), # <-- Nueva ruta de registro
]