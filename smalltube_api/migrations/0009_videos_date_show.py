# Generated by Django 4.2.14 on 2024-12-06 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0008_alter_videos_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='date_show',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
    ]
