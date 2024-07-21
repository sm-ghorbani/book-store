from rest_framework.permissions import IsAuthenticated
from api_tools.api_handler import APILayerHandler
from user.authentication import CustomJWTAuthentication
from core.views import BaseView
from book.adapters import BookAdapter
from .services import SuggestionService


class SuggestionView(BaseView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @APILayerHandler(
        outgoing_adapters=[
            BookAdapter,
        ],
    )
    def get(self, request, **kwargs):
        user_id = request.user.id
        suggestions = SuggestionService.get_user_book_suggestions(user_id)
        return suggestions
