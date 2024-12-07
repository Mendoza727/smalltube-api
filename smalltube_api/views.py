from .serializers import *
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from smalltube_api.utils.sendEmail import send_email
from urllib.parse import urlparse, urlunparse
from user_agents import parse
from .models import *
 
User = get_user_model()

def verify_email(request):
    return render(request, 'verifyEmail.html')

def normalize_email(email):
    return email.strip().lower()

class UserLoginApiView(APIView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request):
        email = request.query_params.get('email')
        if not email:
            raise ValidationError("Email parameter is required.")

        data = {
            'email': email
        }
        serializer = UserLoginSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        if user.is_verified == False:
            return Response({
                "Message": "Debes verificar tu email antes de continuar, revisa tu correo electronico"
            }, status=status.HTTP_401_UNAUTHORIZED)
        

        user_agent = request.META.get('HTTP_USER_AGENT', '')
        parsed_user_agent = parse(user_agent)
        
        deviceInfo = f'os_{parsed_user_agent.os}_browser_{parsed_user_agent.browser}_device_{parsed_user_agent.device}'

        #informacion del dispositivo
        log_data = {
            'device': deviceInfo,
            'created_at': timezone.now(),
            'id_user': user.id
        }

        log_serializer = LogsUserSerializer(data=log_data)

        print("¿Es válido?", log_serializer.is_valid())  # Muestra False
        print("Errores de validación:", log_serializer.errors)  # Muestra los errores detallados

        if log_serializer.is_valid():
            log_serializer.save()
            
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'name': str(user.name),
            'last_name': str(user.last_name),
            'email': str(user.email),
            'avatar': str(user.avatars),
            'role': str(user.role)
        }, status=status.HTTP_200_OK)

class UserRegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserRegisterSerializer
    )
    def post(self, request):
        name = request.data.get('name')
        last_name = request.data.get('last_name')
        email = normalize_email(request.data.get('email'))
        avatars = request.data.get('avatar')
        role = request.data.get('role')

        if role is None:
            role = 'user'

        data = {
            'name': name,
            'last_name': last_name,
            'email': email,
            'avatars': avatars,
            'role': role
        }

        try:
            serializer = UserRegisterSerializer(data=data)

            if serializer.is_valid():
                user_instance = serializer.save()
                print("User successfully registered:", user_instance)

                # enviamos el correo de activacion
                url = request.build_absolute_uri()
                parsed_url = urlparse(url)
                new_path = parsed_url.path.replace('/api', '').replace('/register/', '')
                new_url = parsed_url._replace(path=new_path)
                final_url = urlunparse(new_url)

                sendEmail = send_email(
                    subject="Verifica tu correo",
                    to_email=email,
                    link=f'{final_url}/VerifyEmail/?email={email}'
                )

                if not sendEmail:
                    return Response({
                        'message': f'usuario creado correctamente {serializer.data}'
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "Message": "Correo ya registrado"
                }, status=status.HTTP_302_FOUND)

        except Exception as e:
            Response({
                'ERR': f'Ha ocurrido un error {e}'
            }, status=status.HTTP_403_FORBIDDEN)

class VerifyEmailView(APIView):
    @swagger_auto_schema(auto_schema=None)
    def get(self, request):
        email = request.query_params.get('email')

        if not email: 
            raise ValidationError('Email parameter is required.')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('usuario no encontrado')
        
        # cambiamos el verified
        user.is_verified = True
        user.save()

        return Response({
            email: email,
            'is_verified':user.is_verified
        }, status=status.HTTP_200_OK)

class VideoRegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=VideoSerializer
    )
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        video = request.data.get('video')
        type_video = request.data.get('type_video')
        date_show = request.data.get('date_show')
        categoryId = request.data.get('category'),
        id_autor = request.data.get('id_autor')


        try:
            data = {
                'title': title,
                'description': description,
                'video': video,
                'is_approved': False,
                'type_video': type_video,
                'is_active': True,
                'category': categoryId,
                'id_autor': id_autor,
                'created_at': timezone.now(),
                'modified_at': timezone.now(),
                'date_show': date_show
            }

            serializer = VideoSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'Message': f'The video with title "{title}" has been successfully created.'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'Errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'Error': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    @swagger_auto_schema(request_body=VideoIDSerializer)
    def put(self, request, pk):
        try:
            video_instance = Videos.objects.get(pk)
        except Videos.DoesNotExist:
            return Response({
                'message': 'Video not found'
            }, status=status.HTTP_404_NOT_FOUND)

        video_instance.title = request.data.get('title', video_instance.title)
        video_instance.description = request.data.get('description', video_instance.description)
        video_instance.video = request.data.get('video', video_instance.video)
        video_instance.type_video = request.data.get('type_video', video_instance.type_video)
        video_instance.tags = request.data.get('tags', video_instance.tags)
        video_instance.is_active = request.data.get('is_active', video_instance.is_active)
        video_instance.modified_at = timezone.now()

        video_instance.save()

        # retornamos la respuesta
        return Response({
            'message': "Video editado correctamente"
        }, status=status.HTTP_200_OK)
    

        # eliminando los videos
    @swagger_auto_schema()
    def delete(self, request, pk):
        try:
            video_intance = Videos.objects.get(pk=pk)
        except Videos.DoesNotExist:
            return Response({
                'message': 'Video not fount'
            }, status=status.HTTP_204_NO_CONTENT)
        
        video_intance.delete()

        return Response({
            'message': 'Video eliminated'
        }, status=status.HTTP_204_NO_CONTENT)


class getAllVideos(APIView):
    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all videos from the database"
    )
    def get(self, request, *args, **kwargs):
        try:
            video_instance = Videos.objects.all()

            serializer = VideoSerializer(video_instance, many=True)

            return Response({
                'message': 'videos consultamos correctamente',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'ERR': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class getVideosByAutor(APIView):
    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all videos by a specific author from the database",
    )
    def get(self, request):
        id_autor = request.query_params.get('autor')

        if not id_autor:
            return Response({
                'ERR': 'id_autor is required as a query parameter'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            videos_instance = Videos.objects.filter(id_autor=id_autor)

            serializer = VideoSerializer(videos_instance, many=True)

            return Response({
                'message': 'datos encontrados',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'ERR': f'ha ocurrido un error {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
