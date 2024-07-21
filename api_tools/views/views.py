from rest_framework.views import APIView


class BaseView(APIView):
    validators = []
    incoming_adapters = []
    outgoing_adapters = []
