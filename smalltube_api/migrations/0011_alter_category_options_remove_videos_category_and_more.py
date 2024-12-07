# Generated by Django 4.2.14 on 2024-12-07 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0010_category_notifications_alter_comments_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'categoria', 'verbose_name_plural': 'categorias'},
        ),
        migrations.RemoveField(
            model_name='videos',
            name='category',
        ),
        migrations.AddField(
            model_name='videos',
            name='category',
            field=models.ManyToManyField(to='smalltube_api.category'),
        ),
    ]
