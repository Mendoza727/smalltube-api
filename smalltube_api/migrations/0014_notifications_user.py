# Generated by Django 4.2.14 on 2024-12-07 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0013_delete_videostatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notificacion', to=settings.AUTH_USER_MODEL),
        ),
    ]
