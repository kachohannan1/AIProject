# settings.py
# Add this at the bottom or anywhere in the file:

AUTHENTICATION_BACKENDS = [
    'chatbot.authentication.EmailBackend',  # your custom backend (adjust 'chatbot' if your app has a different name)
    'django.contrib.auth.backends.ModelBackend',  # default backend as fallback
]


DEBUG = True  # True for development, False in production

SECRET_KEY = 'django-insecure-+9(!#k@your-generated-secret-key-1234)'


ALLOWED_HOSTS = ['localhost', '127.0.0.1']

ROOT_URLCONF = 'backend.urls'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',               # Add corsheaders here
    'rest_framework',
    'rest_framework.authtoken',  # For token authentication
    'chatbot',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be first or near top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React app origin (no extra spaces)
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chatbotdb',
        'USER': 'marketingchat',
        'PASSWORD': 'chat123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

STATIC_URL = '/static/'
