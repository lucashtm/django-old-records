from django.contrib import admin
from django_old_records.models import ModelConfig, FieldConfig

class FieldConfigInline(admin.TabularInline):
    model = FieldConfig

class ModelConfigAdmin(admin.ModelAdmin):
    inlines = [FieldConfigInline]

admin.site.register(ModelConfig, ModelConfigAdmin)
