from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('create/', PostCreateApiView.as_view(), name='create-post'),
    path('posts/', PostListApiView.as_view(), name='products-list'),
    path('posts/<int:pk>/', PostDetailDestroyApiView.as_view(), name='detail-post'),
    path('like/<int:pk>/', PostLikeAPIView.as_view(), name='like-post'),
    path('users/', UserListApiView.as_view(), name='list-users'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('user-create/', UserCreateApiView.as_view(), name='user-create')
]