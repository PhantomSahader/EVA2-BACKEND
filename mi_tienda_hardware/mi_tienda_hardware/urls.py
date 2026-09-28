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
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tienda.views import CustomTokenObtainPairView, home_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # 1. Ruta principal: Renderiza directamente tu frontend HTML con Tailwind y Rare UI
    path('', home_view, name='home'),
    
    # 2. Panel de Administración de Django (por si necesitas entrar a crear datos iniciales)
    path('admin/', admin.site.urls),
    
    # 3. Endpoints de la API REST (Conecta la app 'tienda' bajo el prefijo /api/)
    path('api/', include('tienda.urls')),
    
    # 4. Autenticación JWT con claims de rol personalizados (Cliente / Administrador)
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 5. Documentación interactiva Swagger / OpenAPI exigida por la rúbrica
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

]
hadler404 = 'tienda.views.custom_404_view'  # Manejo de errores 404 personalizado