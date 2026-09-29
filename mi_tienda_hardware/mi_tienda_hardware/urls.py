"""
URL configuration for mi_tienda_hardware project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenRefreshView
from tienda.views import (
    CategoriaViewSet, ProductoViewSet, CarroViewSet, OrdenViewSet,
    CustomTokenObtainPairView, home_view, documentacion_view, RegistroClienteView
)

# 1. Enrutador centralizado de la API REST
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'productos', ProductoViewSet, basename='producto')
router.register(r'carro', CarroViewSet, basename='carro')
router.register(r'ordenes', OrdenViewSet, basename='orden')

urlpatterns = [
    # 2. Vista principal del frontend HTML con Tailwind y Rare UI
    path('', home_view, name='home'),
    
    # 3. Vista protegida de documentación (Estrictamente para Admins / Staff)
    path('documentacion/', documentacion_view, name='documentacion'),
    
    # 4. Panel de Administración de Django
    path('admin/', admin.site.urls),
    
    # 5. Endpoints de la API REST bajo el prefijo /api/
    path('api/', include(router.urls)),
    
    # 6. Autenticación JWT y Registro de Clientes con RUT
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/registro/', RegistroClienteView.as_view(), name='registro_cliente'),
    
    # 7. Documentación interactiva Swagger / OpenAPI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# Manejo de error 404 personalizado
handler404 = 'tienda.views.custom_404_view'