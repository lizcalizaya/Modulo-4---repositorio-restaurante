1. Abrir la carpeta del proyecto

Abre la consola dentro de la carpeta principal del proyecto Django, por ejemplo:

C:\Users\USUARIO\modulo04_pedidos


2. Crear/Activar el entorno virtual

python -m venv .venv
.venv\Scripts\activate


3. Instalar todas las dependencias

pip install -r requirements.txt


4. Crear las migraciones

python manage.py migrate
python manage.py makemigrations


5. Superusuario

Debería ser admin - admin 


6. Ejecutar el servidor

Con el entorno virtual activado, correr el proyecto:

python manage.py runserver



URLS PRINCIPALES PARA PROBAR EL SISTEMA


1. MONITOR DE PEDIDOS (Pantalla principal de cocina)

http://127.0.0.1:8000/monitor


2. ADMIN / GESTIÓN COMPLETA DEL SISTEMA

http://127.0.0.1:8000/admin


3. API PARA CREAR Y CONSULTAR PEDIDOS

http://127.0.0.1:8000/api/pedidos/