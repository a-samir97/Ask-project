from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Blog
from .serializers import BlogSerializer, UserSerializer
from rest_framework import generics, permissions
from .permissions import IsAuthorOrReadOnly
# Create your views here.

class BlogList(generics.ListCreateAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    # to save request user to be thr author of the blog
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class UserList(generics.ListCreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
