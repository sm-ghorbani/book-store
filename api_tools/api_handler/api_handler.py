from collections.abc import Iterable
from functools import partial

from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.pagination import BasePagination
from api_tools.adapter import BaseAdapter
from api_tools.validators import BaseValidator, Context


class APILayerHandler:
    def __init__(
        self,
        permissions: list[BasePermission] = [],
        validators: list[BaseValidator] = [],
        incoming_adapters: list[BaseAdapter] = [],
        filter=None,
        outgoing_adapters: list[BaseAdapter] = [],
        pagination_class: BasePagination | None = None,
        status_code=200,
    ):
        self.incoming_adapters = incoming_adapters
        self.outgoing_adapters = outgoing_adapters
        self.validators = validators
        self.permissions = permissions
        self.status_code = status_code
        self.filter = filter
        self.pagination_class = pagination_class

    def __call__(self, func):
        def wrapper(instance, request, *args, **kwargs):
            instance.permission_classes = self.permissions
            instance.check_permissions(request)

            self.incoming_adapters.extend(instance.incoming_adapters)
            self.outgoing_adapters.extend(instance.outgoing_adapters)
            self.validators.extend(instance.validators)
            if (
                hasattr(
                    instance,
                    "pagination_class",
                )
                and not self.pagination_class
            ):
                self.pagination_class = instance.pagination_class
            filter = (
                partial(self.filter, data=request.GET) if self.filter else None
            )  # set filter to None if not provided

            validator_context = Context()
            adapter_context = Context()
            self.__process_validators(
                request,
                args,
                kwargs,
                validators=self.validators,
                validator_context=validator_context,
            )

            kwargs["validator_context"] = validator_context

            adapted_data = self.__process_adapters(
                adapter_context=adapter_context,
                adapters=self.incoming_adapters,
                data=request.data,
            )
            kwargs["adapter_context"] = adapter_context
            kwargs["filter"] = filter
            kwargs["cleaned_data"] = adapted_data
            kwargs["request"] = request
            output_data = func(instance, **kwargs)
            if self.pagination_class:
                paginated_data, paginator = self.__process_pagination(
                    request=request,
                    data=output_data,
                )
                output_data = paginated_data
            adapted_output_data = self.__process_adapters(
                adapter_context=adapter_context,
                adapters=self.outgoing_adapters,
                data=output_data,
            )
            if self.pagination_class:
                return self.__paginate_response(adapted_output_data, paginator)
            if isinstance(adapted_output_data, Response):
                return adapted_output_data
            return Response(data=adapted_output_data, status=self.status_code)

        return wrapper

    def __process_adapters(self, adapters, adapter_context, data):
        many = False
        for adapter in adapters:
            if isinstance(data, Iterable) and not isinstance(data, dict):
                many = True
            adapter_obj = adapter(instance=data, many=many)
            adapter_obj.adapter_context = adapter_context
            data = adapter_obj.data
        return data

    def __process_validators(
        self,
        request,
        args,
        kwargs,
        validators,
        validator_context,
    ):

        for validator in validators:
            validator_obj = validator(request, *args, **kwargs)
            validator_obj.validator_context = validator_context
            validator_obj.is_valid()

    def __process_pagination(self, data, request):
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(data, request)
        return result_page, paginator

    def __paginate_response(self, data, paginator):
        return paginator.get_paginated_response(data)
