# Generated by Django 3.2.4 on 2021-09-20 22:26

from django.db import migrations, models
import django.db.models.deletion
import django_old_records.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_age', models.DurationField()),
                ('content_type', models.ForeignKey(limit_choices_to=django_old_records.models.limit_choices_to, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
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
