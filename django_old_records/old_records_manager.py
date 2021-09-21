from django.db import models
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

class OldRecordsManager(models.Manager):
    DEFAULT_CREATED_AT_FIELD = getattr(settings, 'OLD_RECORDS_DEFAULT_CREATED_AT_FIELD', 'created_at')
    DEFAULT_MAX_AGE = getattr(settings, 'OLD_RECORDS_DEFAULT_MAX_AGE', None)

    def _initialize(self):
        self.model_config = self._get_model_config()

    def _created_at_field(self):
        return getattr(self.model, 'created_at_field', self.DEFAULT_CREATED_AT_FIELD)

    def _get_model_config(self):
        from .models import ModelConfig
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(self.model)
        return ModelConfig.objects.filter(content_type=content_type).prefetch_related('fieldconfig_set').first()

    def _default_max_age(self):
        max_age = getattr(self.model, 'max_age', self.DEFAULT_MAX_AGE)
        if isinstance(max_age, int):
            return timedelta(days=max_age)

        if isinstance(max_age, timedelta):
            return max_age

    def created_at_lookup(self):
        return f'{self._created_at_field()}__lte'

    def _field_config_queries(self, field_config):
        time_limit = timezone.now() - field_config.max_age
        return Q(**{field_config.field_name: field_config.value}), Q(**{self.created_at_lookup(): time_limit})

    def _build_filter_query(self):
        model_max_age = self.model_config.max_age if self.model_config.max_age else self._default_max_age()
        model_time_limit =  timezone.now() - model_max_age
        field_configs = self.model_config.fieldconfig_set.all()
        field_filter_query = None
        model_filter_query = None

        if not field_configs and model_time_limit:
            return Q(**{self.created_at_lookup(): model_time_limit})

        if field_configs:
            value_query, age_query = self._field_config_queries(field_configs[0])
            field_filter_query = value_query & age_query
            model_filter_query = ~value_query

            for field_config in field_configs[1:]:
                value_query, age_query = self._field_config_queries(field_config)
                field_filter_query |= value_query & age_query
                model_filter_query &= ~value_query

        if model_time_limit and model_filter_query:
            model_filter_query &= Q(**{self.created_at_lookup(): model_time_limit})

        if model_time_limit and field_filter_query:
            return model_filter_query | field_filter_query
        return field_filter_query

    def get_queryset(self):

        if not hasattr(self.model, self._created_at_field()):
            return super().get_queryset().none()

        self._initialize()

        if not self.model_config:
            return super().get_queryset().none()

        query = self._build_filter_query()
        if query:
            return super().get_queryset().filter(query)
        return super().get_queryset().none()
