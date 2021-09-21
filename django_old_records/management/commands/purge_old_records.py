from django.core.management.base import BaseCommand
from django_old_records.old_records_manager import OldRecordsManager
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.apps import apps
from django_old_records.models import ModelConfig
from django_old_records.queryset_csv_exporter import QuerySetCSVExporter

class Command(BaseCommand):
    help = u"""Deletes all old records from database"""

    def handle(self, *args, **kwargs):
        content_type_filter_query = Q()

        for app in settings.OLD_RECORDS_MODELS:
            for model_name in settings.OLD_RECORDS_MODELS[app]:
                model = apps.get_model(app_label=app, model_name=model_name)
                content_type_filter_query |= Q(app_label=app, model=model._meta.model_name)
        content_types = ContentType.objects.filter(content_type_filter_query)

        for content_type in content_types:
            model_config = ModelConfig.objects.get(content_type=content_type)
            model = content_type.model_class()
            if hasattr(model, 'old_records') and isinstance(model.old_records, OldRecordsManager):
                self.stdout.write(f'Deleting {model.old_records.count()} {model._meta.app_label}.{model.__name__} old records')
                if model_config.export:
                    filename = f'{model._meta.app_label}_{model._meta.model_name}_old_records.csv'
                    QuerySetCSVExporter(model.old_records.all(), filename).export()
                    self.stdout.write(f'Exported deleted records to {filename}')
                model.old_records.all().delete()
