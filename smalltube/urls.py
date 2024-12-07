from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.static import serve

from django.conf import settings

from .settings import DEBUG, MEDIA_URL, MEDIA_ROOT

from smalltube_api.views import verify_email

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Api para una biblioteca de videos",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="juancamilomendozavillegas14@gmail.com"),
        license=openapi.License(name="Licencia MIT"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),



    path('api/', include('smalltube_api.urls')),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
    path('VerifyEmail/', verify_email, name='user-verify')
]
