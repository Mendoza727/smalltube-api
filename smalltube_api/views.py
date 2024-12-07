from .models import *
from .serializers import *
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.views import APIView
from smalltube_api.utils.sendEmail import send_email
from urllib.parse import urlparse, urlunparse
from user_agents import parse
import json

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
        request_body=VideoSerializer,
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        video = request.data.get('video')
        type_video = request.data.get('type_video')
        date_show = request.data.get('date_show')
        category_data = request.data.get('category')
        id_autor = request.data.get('id_autor')
        
         # Convertir `category` a una lista si llega como string
        try:
            category_ids = json.loads(category_data) if category_data else []
            if not isinstance(category_ids, list) or not all(isinstance(pk, int) for pk in category_ids):
                return Response({"Error": "Invalid category format. Expected a list of integers."}, status=400)
        except (ValueError, TypeError):
            return Response({"Error": "Invalid category format. Expected a valid JSON list."}, status=400)

        # Convertirmos `date_show` a un objeto datetime
        try:
            if date_show:
                date_show = datetime.strptime(date_show, "%Y-%m-%d %H:%M:%S")  # Ajusta el formato si es necesario
                date_show = timezone.make_aware(date_show)  # Asegura que sea timezone-aware
            else:
                date_show = timezone.now()
        except ValueError:
            return Response({"Error": "Invalid date format. Expected 'YYYY-MM-DD HH:MM:SS'."}, status=400)

        # Validamos la fecha de subida
        if not date_show:
            date_show = timezone.now()
        while Videos.objects.filter(date_show=date_show).exists():
            date_show += timedelta(hours=1)

        try:
            data = {
                'title': title,
                'description': description,
                'video': video,
                'is_approved': False,
                'type_video': type_video,
                'is_active': True,
                'category': category_ids,
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

class VideoUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VideoIDSerializer,
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)]
    )
    def put(self, request, pk):
        try:
            video_instance = Videos.objects.get(pk=pk)
        except Videos.DoesNotExist:
            return Response({'message': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Actualizar campos básicos
        video_instance.title = request.data.get('title', video_instance.title)
        video_instance.description = request.data.get('description', video_instance.description)
        video_instance.video = request.data.get('video', video_instance.video)
        video_instance.type_video = request.data.get('type_video', video_instance.type_video)
        video_instance.is_active = request.data.get('is_active', video_instance.is_active)
        video_instance.modified_at = timezone.now()

        # Si se envían nuevas categorías, actualizamos la relación de muchos a muchos
        category_data = request.data.get('category')
        if category_data is not None:
            try:
                # Asumimos que se pasan los IDs de las categorías
                categories = Category.objects.filter(id__in=category_data)
                video_instance.category.set(categories)  # Actualizamos las categorías asociadas
            except Category.DoesNotExist:
                return Response({'message': 'Una o más categorías no existen'}, status=status.HTTP_400_BAD_REQUEST)

        # Guardamos los cambios
        video_instance.save()

        return Response({'message': "Video editado correctamente"}, status=status.HTTP_200_OK)


class VideoDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VideoIDSerializer,
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def delete(self, request, pk):
        try:
            video_instance = Videos.objects.get(pk=pk)
        except Videos.DoesNotExist:
            return Response({'message': 'Video not found'}, status=status.HTTP_404_NOT_FOUND)

        video_instance.is_deleted = True
        video_instance.save()

        return Response({'message': 'Video eliminado'}, status=status.HTTP_204_NO_CONTENT)


class CreateCategorysView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CategorieSerializer,
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        name = request.data.get('name')
        description = request.data.get('description')

        try:
            data = {
                'name': name,
                'description': description,
                'is_read': False,
                'created_at': timezone.now()
            }
        
            serializer = CategorieSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                return Response({
                    'Message': f'The catetory with title "{name}" has been successfully created.'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'Errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            return Response({
                'Error': f'An error occurred: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCategorysView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all categorys the database",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def get(self, request, *args, **kwargs):
        try:
            category_instance = Category.objects.all()

            serializer = CategorieSerializer(category_instance, many=True)

            return Response({
                'message': 'catagorias consultadas correctamente',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'ERR': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCategoryByIdsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve categories by a list of category IDs",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def get(self, request):
        id_categories = request.query_params.get('id_category')

        if not id_categories:
            return Response({
                'ERR': 'id_category is required as a query parameter'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Convertir el parámetro de consulta a una lista de IDs
        try:
            id_categories_list = [int(id) for id in id_categories.split(',')]
        except ValueError:
            return Response({
                'ERR': 'id_category must be a list of integers'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Filtrar las categorías por los IDs proporcionados
            categories_instance = Category.objects.filter(id__in=id_categories_list)

            # Si no se encuentran categorías
            if not categories_instance:
                return Response({
                    'ERR': 'No categories found for the provided IDs'
                }, status=status.HTTP_404_NOT_FOUND)

            # Serializar los resultados
            serializer = CategorieSerializer(categories_instance, many=True)

            return Response({
                'message': 'Categorias encontradas',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'ERR': f'ha ocurrido un error: {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class getAllVideosView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all videos from the database",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
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
         
class getVideosByAutorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all videos by a specific author from the database",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
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

class CreateVisualizationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            request_body=VisualitationSerializer,
            manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        # Obtener el id del usuario autenticado
        user = request.data.get('user_id')
        video_id = request.data.get('video_id')

        if not video_id:
            return Response({"Error": "video_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user:
            return Response({
                'Error': "user_id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Comprobar si la visualización ya existe
        if Visualizations.objects.filter(id_user=user, id_video_id=video_id).exists():
            return Response({"Message": "The user has already viewed this video."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crear nueva visualización
            data = {
                'id_user': user,
                'id_video': video_id,
                'created_at': timezone.now()
            }

            serializer = VisualitationSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                return Response({"Message": "Visualization created successfully."}, status=status.HTTP_201_CREATED)      
            
        except Exception as e:
            return Response({
                'ERR': f'ha ocurrido un error {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CreateLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            request_body=LikeSerializer,
            manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def post(self, request):
        video_id = request.data.get('id_video')
        user_id = request.data.get('id_user')

        # Verificar si el video existe
        try:
            video = Videos.objects.get(id=video_id)
        except Videos.DoesNotExist:
            return Response({
                'ERR': 'El video no existe'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el usuario existe
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({
                'ERR': 'El usuario no existe'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            data = {
                'id_user': user_id,
                'id_video': video_id,
                'created_at': timezone.now()
            }
        
            # Serializar el objeto 'like' recién creado
            serializer = LikeSerializer(data=data)

            if serializer.is_valid():
                serializer.save()

                # enviamos una notificacion
                video = Videos.objects.get(id=video_id)
                Notifications.objects.create(
                    user=video.id_autor,  # El autor del video recibirá la notificación
                    message=f"Tu video '{video.title}' ha recibido un nuevo like.",
                    is_read=False
                )

                return Response({
                    'message': "me gusta creado",
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'ERR': f'ha ocurrido un error {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteLikeView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
            request_body=LikeSerializer,
            manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def delete(self, request):
        # Obtener los parámetros id_user e id_video de la solicitud
        user_id = request.data.get('id_user')
        video_id = request.data.get('id_video')

        # Verificar si los parámetros están presentes
        if not user_id or not video_id:
            return Response({"Error": "id_user and id_video are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si el like existe
        like = Likes.objects.filter(id_user_id=user_id, id_video_id=video_id).first()

        if not like:
            return Response({"Error": "Like not found."}, status=status.HTTP_404_NOT_FOUND)

        # Eliminar el like
        like.delete()
        return Response({"Message": "Like deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class CreateCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=CommentSerializer,
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING
            )
        ]
    )
    def post(self, request):
        # Obtener los datos del request
        user_id = request.data.get('id_user')
        video_id = request.data.get('id_video')
        comment_text = request.data.get('comment')

        # Validar los parámetros
        if not video_id or not user_id or not comment_text:
            return Response({
                'Error': 'Faltan parámetros: id_user, id_video y comment son requeridos.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crear los datos del comentario
            data = {
                'id_user': user_id,
                'id_video': video_id,
                'is_approved': True,
                'comment': comment_text,
            }

            # Serializar los datos
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                # Guardar el comentario en la base de datos
                serializer.save()

                # enviamos una notificacion
                video = Videos.objects.get(id=video_id)
                Notifications.objects.create(
                    user=video.id_autor,  # El autor del video recibirá la notificación
                    message=f"Tu video '{video.title}' ha recibido un nuevo comentario.",
                    is_read=False
                )

                return Response({
                    'message': 'Comentario creado correctamente.',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'Error': 'Datos inválidos.',
                    'details': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'Error': f'Ha ocurrido un error inesperado: {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetCommentsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all comments for id_video on the database",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def get(self, request, video_id):
        comments = Comments.objects.filter(id_video_id=video_id)

        if not comments:
            return Response({
                'message': 'No se encontraron comentarios para este video.'
            }, status=status.HTTP_404_NOT_FOUND)

        try:
            serializer = CommentSerializer(comments, many=True)
            
            return Response({
                'message': 'Comentarios obtenidos correctamente.',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                'ERR': f'ha ocurrido un error {e}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class  EditCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="edit the comment from de database",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def put(self, request, id_video, user_id):
        try:
            comment = Comments.objects.get(id_video=id_video, id_user=user_id)
        except Comments.DoesNotExist:
            return Response({
                'Error': 'Comentario no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el usuario autenticado es el autor del comentario
        if comment.id_user.id != user_id:
            return Response({
                'Error': 'No tiene permisos para editar este comentario.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Actualizar el comentario y fecha de modificacion
        comment.comment = request.data.get('comment', comment.comment)
        comment.modified_at = timezone.now()
        comment.save()

        serializer = CommentSerializer(comment)
        return Response({
            'message': 'Comentario actualizado correctamente.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class DeleteCommentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="delete the comment in the video",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def delete(self, request, comment_id):
        try:
            comment = Comments.objects.get(id=comment_id)
        except Comments.DoesNotExist:
            return Response({
                'Error': 'Comentario no encontrado.'
            }, status=status.HTTP_404_NOT_FOUND)

        # Verificar si el usuario autenticado es el autor del comentario
        if comment.id_user != request.user:
            return Response({
                'Error': 'No tiene permisos para eliminar este comentario.'
            }, status=status.HTTP_403_FORBIDDEN)

        # Eliminar el comentario
        comment.delete()
        return Response({
            'message': 'Comentario eliminado correctamente.'
        }, status=status.HTTP_204_NO_CONTENT)
    
class GetVideoStatisticsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING),
                'data': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'video_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_likes': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_comments': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_views': openapi.Schema(type=openapi.TYPE_INTEGER),
                    }
                )
            }
        )},
        operation_description="Get video statistics (likes, comments, views)",
        manual_parameters=[
            openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
        ]
    )
    def get(self, request, video_id):
        # Verificar si el video existe
        video = Videos.objects.filter(id=video_id, is_active=True, is_deleted=False).first()
        if not video:
            return Response({"message": "Video no encontrado o no activo."}, status=status.HTTP_404_NOT_FOUND)

        # Obtener estadísticas
        total_likes = Likes.objects.filter(id_video=video_id).count()
        total_comments = Comments.objects.filter(id_video=video_id, is_approved=True).count()
        total_views = Visualizations.objects.filter(id_video=video_id).count()

        # Formar la respuesta
        data = {
            "video_id": video_id,
            "total_likes": total_likes,
            "total_comments": total_comments,
            "total_views": total_views
        }
        return Response({
            "message": "Estadísticas obtenidas correctamente.",
            "data": data
        }, status=status.HTTP_200_OK)
    
class GetUserNotificationsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="Retrieve all notifications by user_id",
        manual_parameters=[
            openapi.Parameter(
                'Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, user_id):
        if not user_id:
            return Response({
                'ERR': 'user_id is required as a query parameter'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            notifications_instance = Notifications.objects.filter(user_id=user_id).order_by('-created_at')

            if notifications_instance.exists():
                data = [
                    {
                        'id': notification.id,
                        'message': notification.message,
                        'is_read': notification.is_read,
                        'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Aseguramos que sea serializable
                    }
                    for notification in notifications_instance
                ]

                return Response({
                    'notificaciones': data,
                }, status=status.HTTP_200_OK)

            # Asegúrate de devolver una respuesta si no hay notificaciones
            return Response({
                'message': 'No se encontraron notificaciones.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Convierte el error en texto para hacerlo serializable
            return Response({
                'ERR': str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarkAllNotificationsReadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="marked all notification",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def patch(self, request, user_id):
        notifications = Notifications.objects.filter(user_id=user_id, is_read=False)

        try:
            if notifications.exists():
                notifications.update(is_read=True)
                return Response({'message': 'Todas las notificaciones se han marcado como leídas.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay notificaciones pendientes por leer.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'ERR': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarkAllNotificationsUnreadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="marked all notification",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def path(self, request, user_id):
        notifications = Notifications.objects.filter(user_id=user_id, is_read=True)

        try:
            if notifications.exists():
                notifications.update(is_read=False)
                return Response({'message': 'Todas las notificaciones se han marcado como no leídas.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No hay notificaciones que marcar como no leídas.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
             return Response({
                'ERR': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MarkNotificationReadByIdView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200: VideoSerializer(many=True)},
        operation_description="marked all notification",
        manual_parameters=[
        openapi.Parameter('Authorization', openapi.IN_HEADER, description="Token JWT de autenticación", type=openapi.TYPE_STRING)
    ])
    def patch(self, request, notification_id):
        notification = Notifications.objects.get(id=notification_id)

        try:
            if not notification.is_read:
                notification.is_read = True
                notification.save()
                return Response({'message': f'La notificación con ID {notification_id} se ha marcado como leída.'}, status=status.HTTP_200_OK)
            else:
                notification.is_read = False
                notification.save()
                return Response({'message': f'La notificación con ID {notification_id} se ha marcado como no leída.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'ERR': e,
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
