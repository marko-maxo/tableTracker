from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import permissions

from .extras import *
from .permissionClasses import *

# Create your views here.

secret_key = "jwt_secret_key_123"

class LoginUserView(APIView):
    http_method_names = ["post"]
    authentication_classes = []
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        sent_data = request.data
        try:
            username = sent_data["username"]
            password = sent_data["password"]
            user = User.objects.get(username=username)
            if not user.check_password(password):
                return Response({"error": "Provided credentials are not valid"})
        except Exception as e:
            return Response({"error": "Provided credentials are not valid"})


        response = Response()
        
        token = generate_key_for_user(user, secret_key)
        response.set_cookie(
            key='jwt',
            value=token,
            expires=86400,
            httponly=True,
        )
        response.data = {"success": "Logged in"}
        return response

class LogoutView(APIView):
    http_method_names = ["post"]
    authentication_classes = []
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        response = Response(request)
        response.delete_cookie("jwt")
        response.data = {"success": "Logged out"}
        return response

class UserInfo(APIView):
    http_method_names = ["get"]
    
    def get(self, request, *args, **kwargs):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "success": "Logged in"
            })

class UserInfoOnlyAdmin(APIView):
    http_method_names = ["get"]
    permission_classes = [permissions.IsAdminUser,]

    def get(self, request, *args, **kwargs):
        return Response({
            "ADMIN": "ADMIN",
            "username": request.user.username,
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            })
