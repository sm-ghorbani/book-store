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
        404: {
            "USER_NOT_FOUND": "User not found",
            "BOOK_NOT_FOUND": "Book not found",
            "REVIEW_NOT_FOUND": "Review not found",
        },
        409: {
            "BOOK_ALREADY_RATED_BY_USER": "Book already rated by user",
            "BOOK_NOT_BEEN_RATED_BY_USER": "Book not been rated by user",
        },
    }


class APIException(exceptions.APIException):
    mapper = CoreExceptionMapper()
