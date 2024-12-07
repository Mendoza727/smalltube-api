from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        try:
            user = Users.objects.get(email=email)
            data['user'] = user
        except Users.DoesNotExist:
            raise serializers.ValidationError("User with this email does not exist.")
        return data

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['email', 'name', 'last_name']

    def create(self, validated_data):
        user = Users(
            email=validated_data['email'],
            name=validated_data['name'],
            last_name=validated_data['last_name'],
            is_active=True
        )
        user.set_password(validated_data['email'])
        user.save()
        return user

class LogsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogsLoggin
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
class VideoSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    class Meta:
        model = Videos
        fields = '__all__'
class NotificationSerializer(serializers.Serializer):
    
    class Meta:
        model = Notifications
        fields = '__all__'
class VideoIDSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class VisualitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visualizations
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = '__all__'

class TemplateEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplatesEmails
        fields = '__all__'