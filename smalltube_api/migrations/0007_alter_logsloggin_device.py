# Generated by Django 4.2.14 on 2024-12-05 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0006_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsloggin',
            name='device',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
