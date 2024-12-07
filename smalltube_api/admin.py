from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Users, LogsLoggin, Videos, Visualizations, Likes, TemplatesEmails

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ("name", "last_name", "email", "role", "is_active", 'is_staff', 'is_verified', "created_at", "modified_at")
    list_filter = ("is_active", "role")
    ordering = ["created_at"]

    filter_horizontal = []

    fieldsets = (
        (None, {'fields': ('name', 'last_name', 'email', 'avatars', 'password')}),
        ('Permissions', {'fields': ('is_active', 'groups', 'user_permissions')}),
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"


@admin.register(LogsLoggin)
class AdminLogsLogging(admin.ModelAdmin):
    list_display = (
        'id_user',
        'device',
        'created_at'
    )

    ordering = ['created_at']

    list_filter = (
       [ 'created_at']
    )


    filter_horizontal = []

    class Meta:
        verbose_name = 'log de sesion'
        verbose_name_plural = 'logs de sesiones'