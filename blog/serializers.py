from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Blog

class BlogSerializer(serializers.ModelSerializer):
    #author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Blog
        fields = ('id', 'title', 'body', 'created_at')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username')
