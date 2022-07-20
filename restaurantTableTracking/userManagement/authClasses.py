from .extras import *
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

secret_key = "jwt_secret_key_123"

class JWTCookieUserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user_check = token_user_check(request.COOKIES.get("jwt"), secret_key)
        if user_check == 1:
            raise exceptions.AuthenticationFailed("Token has expired")
        if user_check is not None:
            return (user_check, None)
        raise exceptions.AuthenticationFailed("Authentication failed")
        # return None

