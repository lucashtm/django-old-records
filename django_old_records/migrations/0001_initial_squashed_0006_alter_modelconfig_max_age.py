# Generated by Django 3.2.4 on 2021-09-24 20:19

from django.db import migrations, models
import django.db.models.deletion
import django_old_records.models


class Migration(migrations.Migration):

    replaces = [('django_old_records', '0001_initial'), ('django_old_records', '0002_modelconfig_mode'), ('django_old_records', '0003_alter_modelconfig_content_type'), ('django_old_records', '0004_auto_20210921_1928'), ('django_old_records', '0005_alter_modelconfig_content_type'), ('django_old_records', '0006_alter_modelconfig_max_age')]

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_age', models.DurationField(blank=True, null=True)),
                ('content_type', models.OneToOneField(limit_choices_to=django_old_records.models.limit_choices_to, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('export', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='FieldConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100, validators=[django_old_records.models.validate_field])),
                ('value', models.CharField(max_length=100, validators=[django_old_records.models.validate_field_value])),
                ('max_age', models.DurationField()),
                ('model_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_old_records.modelconfig')),
            ],
        ),
    ]
