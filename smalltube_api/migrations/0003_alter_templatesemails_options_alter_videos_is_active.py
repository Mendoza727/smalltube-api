# Generated by Django 4.2.14 on 2024-12-04 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0002_alter_users_age'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='templatesemails',
            options={'verbose_name': 'plantilla de email', 'verbose_name_plural': 'plantillas de emails'},
        ),
        migrations.AlterField(
            model_name='videos',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='video activo'),
        ),
    ]
