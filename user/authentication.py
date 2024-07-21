from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from .services import UserService


class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        user = UserService.read_one(id=("=", user_id))
        if user is None:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")
        return user

    def authenticate(self, request):
        try:
            raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            if raw_token is None:
                return None
            validated_token = self.get_validated_token(raw_token)
            user, validated_token = self.get_user(validated_token), validated_token
            user.is_authenticated = True
            return user, validated_token
        except Exception as e:
            return None
