from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

# models user
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Debe ingresar un email válido para continuar")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("El superusuario debe tener is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class Users(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    ROLE_CHOICES = [
        ('user', 'Usuario'),
        ('moderator', 'Moderador'),
        ('admin', 'Administrador'),
    ]

    name = models.CharField(max_length=15, verbose_name="nombre de usuario")
    last_name = models.CharField(blank=True, max_length=15, verbose_name="Apellido (opcional)")
    email = models.EmailField(max_length=50, unique=True)
    avatars = models.ImageField(upload_to="avatars/", null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='user', verbose_name="Rol del usuario")
    is_active = models.BooleanField(default=True, verbose_name="usuario activo")
    is_staff = models.BooleanField(default=False, verbose_name="es miembro del staff")
    is_verified = models.BooleanField(default=False, verbose_name="verifico el correo?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    objects = UserManager()

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"

    def __str__(self):
        return f"{self.name} ({self.email})"
    
class LogsLoggin(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="usuario", verbose_name="log usuario")
    device = models.TextField(blank=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "log sesíon"
        verbose_name_plural = "logs sesiones"
    
    def __str__(self):
        return f"Log de {self.id_user.email} - {self.created_at}"

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)


class Videos(models.Model):
    GENERAL_TYPE_VIDEO = [
        ("VT", "Video con Título"),
        ("VBL", "Video con Banner Lateral"),
        ("BT", "Banner con Título")
    ]

    title = models.CharField(blank=False, max_length=50)
    description = models.CharField(blank=True, max_length=150)
    video = models.FileField(upload_to="videos/", null=True, blank=True)
    is_approved = models.BooleanField(default=False, verbose_name="Aprobado por moderador")
    moderation_notes = models.TextField(blank=True, null=True, verbose_name="Notas de moderación")
    type_video = models.CharField(choices=GENERAL_TYPE_VIDEO, verbose_name="Tipo de video", default="VT", max_length=255)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name="videos")
    is_active = models.BooleanField(default=False, verbose_name="video activo")
    is_deleted = models.BooleanField(default=False, verbose_name="Video eliminado")
    id_autor = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Autor del video")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    date_show = models.DateTimeField(verbose_name="Fecha de publicación")

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.title

class Comments(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, verbose_name="Usuario que escribio el mensaje")
    id_video = models.ForeignKey(Videos, on_delete=models.CASCADE, blank=False, verbose_name="Video en el que comento")
    is_approved = models.BooleanField(default=False, verbose_name="Aprobado por moderador")
    comment = models.TextField(max_length=255, blank=True, null=True, verbose_name="comentario")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = 'comentario'
        verbose_name_plural = 'comentarios'

    def __str__(self):
        return f"Comentario de {self.id_user.email} en {self.id_video.title}"

class Visualizations(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, verbose_name="usuario que vio el video")
    id_video = models.ForeignKey(Videos, on_delete=models.CASCADE, blank=False, verbose_name="video que visualizo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "visualizacion"
        verbose_name_plural = "visualizaciones"

    def __str__(self):
        return str(self.id_user)

class Likes(models.Model):
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, verbose_name="usuario que dio like")
    id_video = models.ForeignKey(Videos, on_delete=models.CASCADE, blank=False, verbose_name="video que visualizo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        return str(self.created_at)

class Notifications(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="notificacion"),
    message = models.TextField(verbose_name="Mensaje de notificacion")
    is_read = models.BooleanField(default=True, verbose_name="esta leido?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")

    class Meta:
        verbose_name = "notificacion"
        verbose_name_plural = "notificaciones"
    
    def __str__(self):
        return self.message

class VideoStatistics(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="statistics")
    date = models.DateField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "estadistica de video"
        verbose_name_plural = "estadisticas de los videos"
    
    def __str__(self):
        return f"like {self.likes} views {self.views}"

class TemplatesEmails(models.Model):
    name = models.CharField(blank=False, max_length=255, verbose_name="tipo de email")
    template = models.CharField(blank=False, verbose_name="template", max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    modified_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "plantilla de email"
        verbose_name_plural = "plantillas de emails"
    
    def __str__(self):
        return self.name