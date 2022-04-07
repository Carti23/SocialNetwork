from rest_framework import serializers
from .models import *
from rest_framework.reverse import reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User

from django.conf import settings
import requests

# email hunter function
def hunter_email_verifier(email):
    params = {
        'email': email,
        'api_key': settings.HUNTER_API_KEY
    }
    url = settings.HUNTER_EMAIL_VERIFIER_URL

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {}


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]


# Token Serializer
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def verify_email(self):
        email = self.validated_data['email']

        if settings.HUNTER_API_KEY:
            response = hunter_email_verifier(email)

            if not response['data']['result'] == 'deliverable':
                raise serializers.ValidationError('Invalid email.')

        return email

    # validate password
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs


    # create user object
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

# Post Create Serializer
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('owner', 'title', 'content')

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')


# Post Detail Serializer
class PostDeatilSerializer(serializers.ModelSerializer):
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'pk',
            'title',
            'total_likes',
            'content',
        ]

    # count total likes
    def get_total_likes(self, instance):
        return instance.liked_by.count()

# Post List Serializer
class PostListSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='detail-post',
        lookup_field='pk')
    like_url = serializers.HyperlinkedIdentityField(
        view_name="like-post",
        lookup_field='pk'
    )
    total_likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'owner',
            'pk',
            'liked_by',
            'title',
            'total_likes',
            'content',
            'like_url',

            'url',
        ]

    # add a url to edir post
    def get_edit_url(self, obj):
        request = self.context.get('request')

        if request is None:
            return None
        return reverse('detail-post',  kwargs={"pk": obj.pk}, request=request)

    # add url to like post
    def get_like_url(self, obj):
        request = self.context.get('request')

        if request is None:
            return None
        return reverse('like-post',  kwargs={"pk": obj.pk}, request=request)

    # count total likes
    def get_total_likes(self, instance):
        return instance.liked_by.count()

