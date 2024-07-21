from django.contrib.auth.hashers import check_password
from rest_framework import fields
from api_tools.validators import BaseValidator, FieldValidator
from core.exceptions import APIException
from .services import UserService


class LoginFieldValidator(FieldValidator):
    username = fields.CharField(required=True)
    password = fields.CharField(required=True)


class LoginUsernamePasswordValidator(BaseValidator):

    def validate_request_data(self, **kwargs):
        super().validate_request_data(**kwargs)
        username = kwargs.get("username")
        password = kwargs.get("password")
        user = UserService.read_one(username=username)
        if user and check_password(password, user.password):
            self.validator_context.set("user", user)
        else:
            raise APIException("INVALID_CREDENTIALS")
