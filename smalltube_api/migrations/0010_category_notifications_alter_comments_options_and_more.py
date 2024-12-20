# Generated by Django 4.2.14 on 2024-12-07 01:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('smalltube_api', '0009_videos_date_show'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Mensaje de notificacion')),
                ('is_read', models.BooleanField(default=True, verbose_name='esta leido?')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
            options={
                'verbose_name': 'notificacion',
                'verbose_name_plural': 'notificaciones',
            },
        ),
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': 'comentario', 'verbose_name_plural': 'comentarios'},
        ),
        migrations.AlterModelOptions(
            name='likes',
            options={'verbose_name': 'like', 'verbose_name_plural': 'likes'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name': 'usuario', 'verbose_name_plural': 'usuarios'},
        ),
        migrations.AlterModelOptions(
            name='videos',
            options={'verbose_name': 'video', 'verbose_name_plural': 'videos'},
        ),
        migrations.AlterModelOptions(
            name='visualizations',
            options={'verbose_name': 'visualizacion', 'verbose_name_plural': 'visualizaciones'},
        ),
        migrations.RemoveField(
            model_name='users',
            name='is_admin',
        ),
        migrations.RemoveField(
            model_name='videos',
            name='tags',
        ),
        migrations.AddField(
            model_name='comments',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Aprobado por moderador'),
        ),
        migrations.AddField(
            model_name='users',
            name='role',
            field=models.CharField(choices=[('user', 'Usuario'), ('moderator', 'Moderador'), ('admin', 'Administrador')], default='user', max_length=15, verbose_name='Rol del usuario'),
        ),
        migrations.AddField(
            model_name='videos',
            name='is_approved',
            field=models.BooleanField(default=False, verbose_name='Aprobado por moderador'),
        ),
        migrations.AddField(
            model_name='videos',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='Video eliminado'),
        ),
        migrations.AddField(
            model_name='videos',
            name='moderation_notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notas de moderación'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='modified_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización'),
        ),
        migrations.AlterField(
            model_name='videos',
            name='date_show',
            field=models.DateTimeField(verbose_name='Fecha de publicación'),
        ),
        migrations.CreateModel(
            name='VideoStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('likes', models.PositiveIntegerField(default=0)),
                ('comments', models.PositiveIntegerField(default=0)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='statistics', to='smalltube_api.videos')),
            ],
            options={
                'verbose_name': 'estadistica de video',
                'verbose_name_plural': 'estadisticas de los videos',
            },
        ),
        migrations.AddField(
            model_name='videos',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='videos', to='smalltube_api.category'),
        ),
    ]
