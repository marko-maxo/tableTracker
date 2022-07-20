import jwt
import time
from django.contrib.auth.models import User

def generate_key_for_user(user, secret_key):
    user_data = {
            "id": user.id,
            "username": user.username,
            "iat": time.time(),
            "exp": time.time() + 86400
        }
    return jwt.encode(user_data, secret_key, algorithm='HS256')

def token_check(token, secret_key):
    try:
        data = jwt.decode(token, secret_key, algorithms=['HS256'])
        return data
    except Exception as e:
        print(e)
        return False

def token_user_check(token, secret_key):
    try:
        data = jwt.decode(token, secret_key, algorithms=['HS256'])
        return User.objects.get(id=data['id'])
    except Exception as e:
        print(e)
        return None