Proyecto Django mínimo generado automaticamente.
- Proyecto: gestion_pedidos
- App: mainApp
- API base: /api/pedidos/

Instrucciones rápidas:
1. Crear y activar un virtualenv:
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows

2. Instalar dependencias:
   pip install -r requirements.txt

3. Aplicar migraciones y ejecutar:
   python manage.py migrate
   python manage.py runserver

Nota: Cambia SECRET_KEY en gestion_pedidos/settings.py para producción.
