from rest_framework import serializers

from api_tools.context import Context
from api_tools.exceptions import APIException
from rest_framework import fields


class BaseValidator:
    validator_context: Context | None = None

    def __init__(self, request, *args, **kwargs) -> None:
        self.request = request
        self.path_parameters = kwargs

    def validate_request_data(self, **kwargs):
        pass

    def validate_query_params(self, query_params):
        pass

    def validate_request(self, request):
        self.validate_query_params(query_params=request.query_params)
        self.validate_request_data(**request.data)

    def validate_path_params(self, **kwargs):
        pass

    def is_valid(self):
        self.validate_request(self.request)
        self.validate_path_params(**self.path_parameters)
        return True


class _BaseFieldValidator(BaseValidator):
    def __init__(self, request, *args, **kwargs) -> None:
        super().__init__(request, *args, **kwargs)
        self._declared_fields = self._get_declared_fields()

    def _reject_extra_fields(self, incoming_fields):
        extra_fields = set(incoming_fields.keys()) - set(
            self._declared_fields.keys()
        )  # get extra fields
        if extra_fields:
            raise serializers.ValidationError(
                f"Extra fields are not allowed: {extra_fields}"
            )

    def _get_declared_fields(self):
        declared_fields = {}
        for field_name, field_instance in vars(self.__class__).items():
            if isinstance(field_instance, fields.Field):
                declared_fields[field_name] = field_instance
        return declared_fields


class FieldValidator(_BaseFieldValidator):
    serializer = serializers.Serializer

    @property
    def dynamic_serializer(self):
        meta_class = getattr(self, "Meta", type("Meta", (), {}))
        return type(
            "DynamicSerializer",
            (self.serializer,),
            {
                "Meta": meta_class,
                **self._declared_fields,
            },
        )

    def validate_request_data(self, **kwargs):
        super().validate_request_data(**kwargs)

        self._reject_extra_fields(
            incoming_fields=kwargs,
        )

        serializer = self.dynamic_serializer(data=kwargs)

        serializer.is_valid(raise_exception=True)


class ModelFieldValidator(FieldValidator):
    serializer = serializers.ModelSerializer

    def _reject_extra_fields(self, incoming_fields):
        extra_fields = set(incoming_fields.keys()) - set(self.Meta.fields)
        if extra_fields:
            raise serializers.ValidationError(
                f"Extra fields are not allowed: {extra_fields}"
            )


class QueryParamsValidator(_BaseFieldValidator):

    def validate_query_params(self, query_params):
        errors = {"query_param_errors": {}}

        for field_name, field_instance in self._declared_fields.items():
            if field_instance.required:
                try:
                    setattr(
                        self,
                        field_name,
                        field_instance.run_validation(
                            data=query_params.get(field_name),
                        ),
                    )
                except fields.ValidationError as e:
                    errors["query_param_errors"][field_name] = e.detail
        if errors["query_param_errors"]:
            raise APIException(code=400, detail=errors)
