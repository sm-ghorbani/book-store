import jwt
import datetime
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from api_tools.api_handler import APILayerHandler
from core.views import BaseView
from .validators import LoginFieldValidator, LoginUsernamePasswordValidator


class LoginView(BaseView):

    @APILayerHandler(
        validators=[
            LoginFieldValidator,
            LoginUsernamePasswordValidator,
        ]
    )
    def post(self, request, validator_context, **kwargs):
        user = validator_context.get("user")
        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.now()
            + datetime.timedelta(
                seconds=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
            ),
            "iat": datetime.datetime.now(),
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.set_cookie(
            "access",
            token,
            max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
            path=settings.AUTH_COOKIE_PATH,
            secure=settings.AUTH_COOKIE_SECURE,
            httponly=settings.AUTH_COOKIE_HTTP_ONLY,
            samesite=settings.AUTH_COOKIE_SAMESITE,
        )
        return response
