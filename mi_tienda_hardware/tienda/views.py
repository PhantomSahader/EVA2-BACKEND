from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Categoria, Producto, Carro, ItemCarro, Orden, DetalleOrden, PerfilCliente
from .serializers import (
    CategoriaSerializer, ProductoSerializer, CarroSerializer,
    OrdenSerializer, CustomTokenObtainPairSerializer
)

# Vista para manejar el login JWT con claims personalizados de rol
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Vista para el registro público de clientes con RUT
class RegistroClienteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        rut = request.data.get('rut')

        if not username or not email or not password or not rut:
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "El nombre de usuario ya está en uso."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            PerfilCliente.objects.create(user=user, rut=rut)
            return Response({"mensaje": "¡Usuario registrado con éxito!"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Permiso personalizado: Solo administradores (is_staff) pueden escribir, los demás solo lectura
class EsAdministradorOReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [EsAdministradorOReadOnly]

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [EsAdministradorOReadOnly]

class CarroViewSet(viewsets.ModelViewSet):
    serializer_class = CarroSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        carro, _ = Carro.objects.get_or_create(usuario=self.request.user)
        return Carro.objects.filter(usuario=self.request.user)

    @action(detail=False, methods=['post'])
    def agregar_item(self, request):
        usuario = request.user
        producto_id = request.data.get('producto')
        cantidad = int(request.data.get('cantidad', 1))

        carro, _ = Carro.objects.get_or_create(usuario=usuario)
        try:
            producto = Producto.objects.get(id=producto_id)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        item, created = ItemCarro.objects.get_or_create(carro=carro, producto=producto)
        if not created:
            item.cantidad += cantidad
        else:
            item.cantidad = cantidad
        item.save()

        serializer = self.get_serializer(carro)
        return Response(serializer.data)

class OrdenViewSet(viewsets.ModelViewSet):
    serializer_class = OrdenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Orden.objects.all()
        return Orden.objects.filter(usuario=user)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        usuario = request.user
        try:
            carro = Carro.objects.get(usuario=usuario)
        except Carro.DoesNotExist:
            return Response({"error": "No hay carro activo."}, status=status.HTTP_400_BAD_REQUEST)

        items = carro.items.all()
        if not items.exists():
            return Response({"error": "El carro está vacío."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            total = sum(item.cantidad * item.producto.precio for item in items)
            
            # Verificar stock de forma atómica
            for item in items:
                if item.producto.stock < item.cantidad:
                    return Response({"error": f"Stock insuficiente para {item.producto.nombre}."}, status=status.HTTP_400_BAD_REQUEST)

            # Crear orden
            orden = Orden.objects.create(usuario=usuario, total=total, estado='PAGADO')

            # Descontar stock y registrar detalles
            for item in items:
                producto = item.producto
                producto.stock -= item.cantidad
                producto.save()

                DetalleOrden.objects.create(
                    orden=orden,
                    producto=producto,
                    cantidad=item.cantidad,
                    precio_unitario=producto.precio
                )

            # Vaciar carro tras la compra exitosa
            carro.items.all().delete()

        return Response({"mensaje": "¡Compra procesada con éxito!", "orden_id": orden.id}, status=status.HTTP_201_CREATED)

# Vista principal del e-commerce
def home_view(request):
    return render(request, 'tienda/index.html')

# Vista protegida: Solo accesible por Administradores (is_staff) por motivos legales y de seguridad
@staff_member_required(login_url='/')
def documentacion_view(request):
    return render(request, 'tienda/documentacion.html')
from django.http import HttpResponse

# Opción 2: Manejo de Error 404 con respuesta directa (sin requerir archivo html externo)
def custom_404_view(request, exception):
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Página No Encontrada | 404</title>
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-100 text-slate-800 font-sans min-h-screen flex items-center justify-center">
        <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-xl text-center max-w-md space-y-4">
            <div class="bg-indigo-50 text-indigo-600 font-mono text-xs font-bold px-3 py-1 rounded-full w-fit mx-auto">Error 404</div>
            <h1 class="text-2xl font-black text-slate-900">Página no encontrada</h1>
            <p class="text-xs text-slate-500">La ruta a la que intentas acceder no existe en el sistema de la tienda de hardware.</p>
            <a href="/" class="inline-block bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold px-5 py-3 rounded-xl transition shadow-md shadow-indigo-600/20">
                Volver al Inicio
            </a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content, status=404)