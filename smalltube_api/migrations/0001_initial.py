# Generated by Django 4.2.14 on 2024-12-04 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('name', models.CharField(max_length=15, verbose_name='nombre de usuario')),
                ('last_name', models.CharField(blank=True, max_length=15, verbose_name='Apellido (opcional)')),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('age', models.IntegerField(verbose_name='Edad')),
                ('avatars', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('is_active', models.BooleanField(default=True, verbose_name='usuario activo')),
                ('is_staff', models.BooleanField(default=False, verbose_name='es miembro del staff')),
                ('is_admin', models.BooleanField(default=False, verbose_name='es administrador')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
            },
        ),
        migrations.CreateModel(
            name='TemplatesEmails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='tipo de email')),
                ('template', models.CharField(max_length=255, verbose_name='template')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
            ],
            options={
                'verbose_name': 'html email',
                'verbose_name_plural': 'html emails',
            },
        ),
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=150)),
                ('video', models.CharField(max_length=255, verbose_name='Url video')),
                ('type_video', models.CharField(choices=[('VT', 'Video con Título'), ('VBL', 'Video con Banner Lateral'), ('BT', 'Banner con Título')], default='VT', max_length=255, verbose_name='Tipo de video')),
                ('tags', models.JSONField(blank=True, max_length=255, verbose_name='Tags')),
                ('is_active', models.BooleanField(default=False, verbose_name='usuario activo')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('id_autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Autor del video')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
        migrations.CreateModel(
            name='Visualizations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario que vio el video')),
                ('id_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smalltube_api.videos', verbose_name='video que visualizo')),
            ],
            options={
                'verbose_name': 'Visualizacion',
                'verbose_name_plural': 'Visualizaciones',
            },
        ),
        migrations.CreateModel(
            name='LogsLoggin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.TextField(blank=True, max_length=80)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario', to=settings.AUTH_USER_MODEL, verbose_name='log usuario')),
            ],
            options={
                'verbose_name': 'log sesíon',
                'verbose_name_plural': 'logs sesiones',
            },
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario que dio like')),
                ('id_video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smalltube_api.videos', verbose_name='video que visualizo')),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'likes',
            },
        ),
    ]
