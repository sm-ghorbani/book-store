from api_tools.views import BaseView as APIView


class BaseView(APIView):
    class Meta:
        abstract = True
