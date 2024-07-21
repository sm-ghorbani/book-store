from rest_framework import serializers

from api_tools.context import Context


class BaseAdapter:
    adapter_context: Context | None = None

    def __init__(self, instance, many=False) -> None:
        self.instance = instance
        self.many = many

    def manipulate_data(self, instance):
        return instance

    @property
    def data(self):
        if self.many:
            return [self.manipulate_data(item) for item in self.instance]
        return self.manipulate_data(self.instance)


class FieldAdapter(serializers.Serializer):
    _data = None

    @property
    def data(self):
        if self._data is None and self.instance is not None:
            self._data = self.manipulate_data(self.instance)
        return self._data

    def manipulate_data(self):
        return self.to_representation(self.instance)


class ModelFieldAdapter(serializers.ModelSerializer):
    _data = None

    @property
    def data(self):
        if self._data is None and self.instance is not None:
            self._data = self.manipulate_data(self.instance)
        return self._data

    def manipulate_data(self, instance):
        return self.to_representation(instance)
