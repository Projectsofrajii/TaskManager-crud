from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.utils.timezone import now


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {
                "password": {"write_only": True},
                "user": {"required": False}
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and set last_login"""
        user = User.objects.create_user(**validated_data)
        user.last_login = now()  
        user.save()
        return user
    
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ["id", "title_id",  "title","description","status"]
