from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = u"""Deletes all old records from database"""

    def handle(self, *args, **kwargs):
        models = apps.get_models()
        for model in models:
            if hasattr(model, 'old_records'):
                self.stdout.write(f'Deleting {model} old records')
                model.old_records.all().delete()
