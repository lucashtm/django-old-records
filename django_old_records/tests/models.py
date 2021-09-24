from django.db import models
from datetime import timedelta
from django_old_records import OldRecordsManager

class HardCodedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    boolean_field = models.BooleanField(default=True)
    max_age = timedelta(seconds=20)
    objects = models.Manager()
    old_records = OldRecordsManager()

class ModelWithConfig(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    boolean_field = models.BooleanField(default=True)
    integer_field = models.IntegerField(default=0)

    objects = models.Manager()
    old_records = OldRecordsManager()

class ModelWithNoCreatedAt(models.Model):
    max_age = timedelta(seconds=20)
    objects = models.Manager()
    old_records = OldRecordsManager()

class ModelWithNoMaxAge(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    old_records = OldRecordsManager()

class ModelWithIntegerMaxAge(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    boolean_field = models.BooleanField(default=True)
    max_age = 5
    objects = models.Manager()
    old_records = OldRecordsManager()
