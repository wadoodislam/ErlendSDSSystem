DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

ALLOWED_HOSTS = ['127.0.0.1']

MACHINE_URL = f'http://{ALLOWED_HOSTS[0]}/'
