from api_tools import exceptions


class CoreExceptionMapper(exceptions.ExceptionMapper):
    exceptions = {
        400: {
            "INVALID_ROLE": "Invalid role",
            "INVALID_QUERY_PARAMS": "Invalid query_params",
        },
        401: {
            "INVALID_CREDENTIALS": "Invalid Credentials",
        },
    }


class APIException(exceptions.APIException):
    mapper = CoreExceptionMapper()
