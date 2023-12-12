from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from drf_social_oauth2.views import ConvertTokenView
from social_django.models import UserSocialAuth  # Import the UserSocialAuth model
from vasitypro.settings import SOCIAL_AUTH_GOOGLE_OAUTH2_KEY, SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
import jwt
import requests
from .models import Project

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('uuid', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
class CustomConvertTokenView(ConvertTokenView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        authorization_code = request.data.get('code')  # Authorization code received from client
        id_token = self.get_and_decode_id_token(authorization_code)  # Use self to call the method

        if id_token:
            user = request.user
            social_account = user.usersocialauth_set.get(provider='google')  # Replace with your actual table name
            social_account.extra_data.update(id_token)  # Save decoded token data to extra_data
            social_account.save()

        return response

    def get_and_decode_id_token(self, authorization_code):
        token_url = 'https://oauth2.googleapis.com/token'
        client_id = SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
        client_secret = SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET
        redirect_url = 'your_redirect_url'

        token_data = {
            'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_url': "http://localhost:8000/accounts/google/login/callback/",
            'grant_type': 'authorization_code'
        }

        response = requests.post(token_url, data=token_data)
        token_info = response.json()

        id_token = token_info.get('id_token')
        if id_token:
            decoded_id_token = jwt.decode(id_token, verify=False)  # You should validate the token in production
            return decoded_id_token
        else:
            return None

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
