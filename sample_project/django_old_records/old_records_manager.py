from django.db import models
from datetime import datetime, timedelta

class OldRecordsManager(models.Manager):
    DEFAULT_CREATED_AT_FIELD = 'created_at'
    DEFAULT_MAX_AGE = None

    def _created_at_field(self):
        return getattr(self.model, 'created_at_field', self.DEFAULT_CREATED_AT_FIELD)

    def _max_age_timedelta(self):
        max_age = getattr(self.model, 'max_age', self.DEFAULT_MAX_AGE)
        if isinstance(max_age, int):
            return timedelta(days=max_age)

        if isinstance(max_age, timedelta):
            return max_age

    def get_queryset(self):
        if not (hasattr(self.model, self._created_at_field()) and self._max_age_timedelta()):
            return self.none()

        time_limit = datetime.now() - self._max_age_timedelta()
        filter_key = f'{self._created_at_field()}__lte'
        return super().get_queryset().filter(**{filter_key: time_limit})
