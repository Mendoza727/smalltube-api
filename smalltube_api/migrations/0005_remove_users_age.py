# Generated by Django 4.2.14 on 2024-12-04 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0004_users_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='age',
        ),
    ]
