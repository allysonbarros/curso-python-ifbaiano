# -*- coding: utf-8 -*-

"""
Arquivo modelo do settings.py.
Aqui deve conter apenas o que há de diferente em relação ao settings_base.py,
como por exemplo senhas e outros dados sigilosos.
"""

try:
    from settings_base import *
except ImportError, e:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/emails/sisbiblioteca/'
