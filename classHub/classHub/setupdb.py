import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if 'DYNO' in os.environ:
    django_db = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd8usk956i31d64',
        'HOST': 'ec2-50-19-227-171.compute-1.amazonaws.com',
        'USER': 'lnpnrhepbtabkt',
        'PASSWORD': 'Wy3753XYgrQleJLits3xz84jCp',
        'PORT': '5432',
        'STATIC_STORAGE': 'whitenoise.django.GzipManifestStaticFilesStorage'
    }
else:
    django_db = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'HOST': '',
        'USER': '',
        'PASSWORD': '',
        'PORT': '',
        'STATIC_STORAGE': None,
    }

SECRET_KEY = 'g^q=9zzoao$s_i4@b+@-vg5v8mknm)pt@wkqeaz_y!64^r8_c8'
