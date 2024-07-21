from rest_framework.exceptions import APIException as DRFExceptions  # noqa


class ExceptionMapper:
    exceptions = {}

    def get_status_and_detail(self, exception_code):
        for status_code, exceptions_mapping in self.exceptions.items():
            for code, detail in exceptions_mapping.items():
                if code == exception_code:
                    return status_code, detail

        raise ValueError(f"exception_code {exception_code} not found")


class APIException(DRFExceptions):
    mapper = ExceptionMapper()

    def __init__(
        self,
        exception_code=None,
        detail=None,
        code=None,
    ):
        if exception_code:
            self.exception_code = exception_code
            code, detail = self.mapper.get_status_and_detail(exception_code)
            self.status_code = code
            super().__init__(detail=detail, code=code)
        self.status_code = code
        super().__init__(detail=detail, code=code)
