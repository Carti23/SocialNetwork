from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from .models import Post

# Login Api View
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

# Register Api View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.verify_email()
        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)
    

# Post Create Api View
class PostCreateApiView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated, ]

    # post function
    def post(self, request, *args, **kwargs):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(owner = request.user)
            return Response(serializer.data, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)


class UserCreateApiView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, ]


# List Products API View
class PostListApiView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [AllowAny, ]

# Detail Post API View (only owner can change the information)
class PostDetailDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = "pk"
    serializer_class = PostDeatilSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# Post Like API View
class PostLikeAPIView(APIView):

    # get function
    def get(self, request, pk):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=pk)
            if request.user in post.liked_by.all():
                post.liked_by.remove(request.user)
            else:
                post.liked_by.add(request.user)
            post.save()
            return Response({'success': True})
        else:
            return Response({'success': False})

# User List Api View
class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
