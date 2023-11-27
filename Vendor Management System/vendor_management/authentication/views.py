# authentication/views.py

from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User  
from .serializers import UserSerializer
from django.contrib.auth.hashers import check_password

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class Registration(APIView):

    def post(self, request, format=None):
        try:
            data_user = {
                'email': request.data.get('email'),
                'name': request.data.get('name'),
                'password': make_password(request.data.get('password')),
                'is_staff': request.data.get('is_staff', False),
                'username': request.data.get('username'),
            }
            
            serializer = UserSerializer(data=data_user)

            if serializer.is_valid():
                user = serializer.save()
                print(user)
                token = get_tokens_for_user(user)
                return Response({"Message": "Registration Successful!", "data": token}, status=status.HTTP_200_OK)
            
            return Response({"Message": "Something went wrong!", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"Message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Custom authentication logic
            user = User.objects.filter(email=email).first()
           
            if user is None or not check_password(password, user.password):
                return Response({"Message": "Incorrect Credentials!", "data": None}, status=status.HTTP_404_NOT_FOUND)

            token = get_tokens_for_user(user)
            return Response({"Message": "Login Successful!", "data": token}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            if isinstance(e, ValidationError):
                return Response({"Message": "Please enter correct credentials!", "data": None}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Message": str(e), "data": None}, status=status.HTTP_400_BAD_REQUEST)
