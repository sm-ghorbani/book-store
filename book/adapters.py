from api_tools.adapter import BaseAdapter


class BookAdapter(BaseAdapter):

    def manipulate_data(self, instance):
        return instance.__dict__
