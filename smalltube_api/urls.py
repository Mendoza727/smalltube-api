from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginApiView.as_view(), name='user-login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('verify/', VerifyEmailView.as_view(), name="verify"),
    path('video/', VideoRegisterView.as_view(), name="create-video"),
    path('get-all-videos/', getAllVideos.as_view(), name="get-all-videos"),
    path('get-video-by-autor/', getVideosByAutor.as_view(), name="get-video-by-autor")
]
