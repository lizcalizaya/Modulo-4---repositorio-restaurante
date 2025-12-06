from pathlib import Path
import os
import dj_database_url # Necesaria si usas PostgreSQL, pero la incluimos

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. SEGURIDAD: CAMBIA ESTO EN PRODUCCIÓN y usa una variable de entorno
SECRET_KEY = os.environ.get('SECRET_KEY', 'cambia-esto-en-produccion')

# 2. SEGURIDAD: DEBUG DEBE SER FALSE EN PRODUCCIÓN
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# 3. SEGURIDAD: DOMINIOS PERMITIDOS
ALLOWED_HOSTS = [
    'modulo-4-repositorio-restaurante-1.onrender.com', 
    '127.0.0.1', 
    'localhost', 
]

# 4. APLICACIONES INSTALADAS (Verificado)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Librerías de terceros
    'rest_framework', 
    
    # Tu app
    'appPedidos', 
]

# 5. MIDDLEWARE CON WHITENOISE (Para servir estáticos en producción)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # <-- AÑADIDO PARA ESTÁTICOS
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'modulo04_pedidos.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',    # carpeta templates/ en la raíz
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'modulo04_pedidos.wsgi.application'

# 6. CONFIGURACIÓN DE BASE DE DATOS PARA SQLite
# Si necesitas usar PostgreSQL en Render, esta sección debe cambiar
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 7. ARCHIVOS ESTÁTICOS (CONFIGURACIÓN DE PRODUCCIÓN)
STATIC_URL = '/static/'

# Directorios donde Django buscará archivos estáticos en desarrollo.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Directorio donde collectstatic los reunirá para producción.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# 8. ALMACENAMIENTO DE ARCHIVOS ESTÁTICOS (WhiteNoise)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage' 

# Resto de la configuración
AUTH_PASSWORD_VALIDATORS = [] 
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Corregido el nombre
