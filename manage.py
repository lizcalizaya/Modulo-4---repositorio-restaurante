<<<<<<< HEAD

=======
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836
import os
import sys

if __name__ == '__main__':
<<<<<<< HEAD
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulo04_pedidos.settings')
=======
    # CAMBIO CRÍTICO: Apunta al módulo de configuración correcto
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'modulo04_pedidos.settings') 
>>>>>>> 67ce92b636632aa62be6ec27ba7a04f024838836

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
