import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import Users

class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # 1. Grab the token from the headers
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None # No token found, move on

        token = auth_header.split(' ')[1]

        try:
            # 2. Decode the token using your secret key
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('توکن منقضی شده است. لطفا دوباره وارد شوید.')
        except jwt.DecodeError:
            raise AuthenticationFailed('توکن نامعتبر است.')

        # 3. Find the user in your custom MySQL database
        user = Users.objects.filter(user_id=payload.get('user_id')).first()
        if not user:
            raise AuthenticationFailed('کاربر یافت نشد.')

        # 4. Attach the user and token to the request
        return (user, token)