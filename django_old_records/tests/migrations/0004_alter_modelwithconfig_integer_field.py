# Generated by Django 3.2.4 on 2021-09-23 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0003_auto_20210923_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelwithconfig',
            name='integer_field',
            field=models.IntegerField(default=0),
        ),
    ]
