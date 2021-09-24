from boot_django import boot_django
from django.core.management import call_command

boot_django()
call_command('squashmigrations', 'django_old_records', '0001', '0006')
