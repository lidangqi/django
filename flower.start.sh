DJANGO_SETTINGS_MODULE=settings.local celery -A recruitment flower --broker=redis://localhost:6379/0
