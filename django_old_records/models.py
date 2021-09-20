from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q

def validate_field(value):
    print(value, type(value))

def validate_field_value(value):
    print(value, type(value))

def limit_choices_to():
    query_filter = Q()
    for key in settings.OLD_RECORDS_MODELS:
        for model_name in settings.OLD_RECORDS_MODELS[key]:
            model = apps.get_model(app_label=key, model_name=model_name)
            query_filter |= Q(app_label=model._meta.app_label, model=model._meta.model_name)
    return query_filter

class ModelConfig(models.Model):

    content_type = models.ForeignKey(
        ContentType,
        limit_choices_to=limit_choices_to,
        on_delete=models.CASCADE,
    )
    max_age = models.DurationField()

class FieldConfig(models.Model):

    model_config = models.ForeignKey('ModelConfig', on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100, validators=[validate_field])
    value = models.CharField(max_length=100, validators=[validate_field_value])
    max_age = models.DurationField()
