from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# filepath: /Users/umutaraz/Desktop/Tüm hayatım burda/CustomerANDvehicleManagement/tamir_takip/tamir_takip/settings.py
STATICFILES_DIRS = [
    BASE_DIR / "static",
    BASE_DIR / "core/static", #tamir_takip değil core uygulamasının içindeki static dosyaları
]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-0-p#)v(t1k3!&kek!m@wdlo+@^(rek@=i#3@9o%6bejak+^d4y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # False yapmayı unutmayın üretim ortamına geçtiğinizde!

ALLOWED_HOSTS = ['*'] # '*' ekle burda yıldız ekleyerek herkese açık hale getir.


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'django_adminlte3',
    'rest_framework', 
    'crispy_forms',
    'crispy_bootstrap5',
    
]
# Crispy Forms ayarlarını bu şekilde yapıyoruz. (hata verirse burayı değiştir)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tamir_takip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  
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

WSGI_APPLICATION = 'tamir_takip.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'tr'  # Türkçe dili tercih edebilirsiniz

TIME_ZONE = 'UTC'  # Türkiye saat dilimine göre 'Europe/Istanbul' yapabilirsiniz

USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Eğer yerel statik dosyalarınız varsa, STATICFILES_DIRS ile dosya yolunu belirleyebilirsiniz.
# STATICFILES_DIRS = [BASE_DIR / "static"] 

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Log out redirect
#LOGOUT_REDIRECT_URL = 'login'  # Çıkış yaptıktan sonra kullanıcı login sayfasına yönlendirilir.

