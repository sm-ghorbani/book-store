from api_tools.api_handler import APILayerHandler
from core.views import BaseView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from user.authentication import CustomJWTAuthentication
from .services import ReviewService
from .validators import (
    ReviewCreateFieldValidator,
    ReviewUpdateFieldValidator,
    ReviewDeleteFieldValidator,
    BookExistsValidator,
    BookNotAlreadyRatedByUserValidator,
    BookBeenRatedByUserValidator,
)


class ReviewCreateUpdateDeleteView(BaseView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsAuthenticated]

    @APILayerHandler(
        validators=[
            ReviewCreateFieldValidator,
            BookExistsValidator,
            BookNotAlreadyRatedByUserValidator,
        ],
    )
    def post(self, request, cleaned_data, **kwargs):
        user_id = request.user.id
        book_id = cleaned_data.get("book_id")
        rating = cleaned_data.get("rating")
        ReviewService.create(
            user_id=user_id,
            book_id=book_id,
            rating=rating,
        )
        return Response(status=status.HTTP_201_CREATED)

    @APILayerHandler(
        validators=[
            ReviewUpdateFieldValidator,
            BookBeenRatedByUserValidator,
        ]
    )
    def patch(self, request, cleaned_data, **kwargs):
        user_id = request.user.id
        book_id = cleaned_data.get("book_id")
        rating = cleaned_data.get("rating")
        ReviewService.update(
            {
                "rating": rating,
            },
            user_id=("=", user_id),
            book_id=("=", book_id),
        )
        return Response(status=status.HTTP_200_OK)

    @APILayerHandler(
        validators=[
            ReviewDeleteFieldValidator,
            BookBeenRatedByUserValidator,
        ]
    )
    def delete(self, request, **kwargs):
        user_id = request.user.id
        book_id = request.data.get("book_id")
        ReviewService.delete(
            user_id=("=", user_id),
            book_id=("=", book_id),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
