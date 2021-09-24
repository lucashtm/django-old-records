# Generated by Django 3.2.4 on 2021-09-24 20:53

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_hardcodedmodel_boolean_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelWithNoCreatedAt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ModelWithNoMaxAge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            managers=[
                ('old_records', django.db.models.manager.Manager()),
            ],
        ),
    ]
