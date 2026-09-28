EVA 2 Backend — PC Hardware Store (DRF + PostgreSQL + JWT)
Aplicación web e-commerce orientada a la venta de componentes de PC, desarrollada bajo una arquitectura de backend robusta con Django REST Framework (DRF), persistencia relacional en PostgreSQL, autenticación segura mediante JWT con claims de roles personalizados, y una interfaz de usuario moderna basada en Tailwind CSS (Rare UI).

🚀 Características Principales
Autenticación JWT Avanzada: Sistema de login y generación de tokens con inyección de roles de usuario (is_staff / Administrador vs. Cliente).

Control Estricto de Roles y Permisos:

Administrador: Capacidad de crear, actualizar y gestionar el catálogo de productos directamente desde la interfaz web, además de visualizar el historial global de órdenes.

Cliente: Registro público interactivo (con validación de nombre, correo, RUT y contraseña), navegación del catálogo, carro de compras persistente en base de datos, ejecución de checkout y visualización de historial de órdenes propio.

Integridad Transaccional: Procesamiento de compras (checkout) protegido mediante transacciones atómicas (transaction.atomic()) para garantizar el descuento concurrente y seguro del stock en PostgreSQL.

Manejo de Errores Personalizado: Vista 404 personalizada y amigable para rutas no encontradas.

🛠️ Stack Tecnológico
Backend: Python, Django, Django REST Framework, SimpleJWT.

Base de Datos: PostgreSQL (tiendahardware_db).

Frontend: HTML5, JavaScript Asíncrono (Fetch API), Tailwind CSS (Rare UI).

Documentación API: DRF Spectacular (Swagger UI).
