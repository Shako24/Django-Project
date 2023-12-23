# vercel_handler.py

from django.core.management import call_command


def handler(req, res):
    # Run Django migrations on deployment
    call_command('migrate', '--noinput')

    # Run the Django application
    call_command('runserver', '0.0.0.0:8080')
