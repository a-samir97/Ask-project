from django.contrib.auth import get_user_model
from .models import Blog
from .serializers import BlogSerializer, UserSerializer
from rest_framework import viewsets


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
