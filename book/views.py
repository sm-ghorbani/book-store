from rest_framework.permissions import IsAuthenticated
from api_tools.api_handler import APILayerHandler
from core.views import BaseView
from user.authentication import CustomJWTAuthentication
from .services import BookService
from .adapters import BookAdapter


class BookListView(BaseView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @APILayerHandler(
        outgoing_adapters=[BookAdapter],
    )
    def get(self, request, **kwargs):
        genre = request.GET.get("genre")
        if genre:
            books = BookService.like("genre", genre)
        else:
            books = BookService.read_all()
        return books
