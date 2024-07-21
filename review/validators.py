from rest_framework import serializers
from api_tools.validators import BaseValidator, FieldValidator
from core.exceptions import APIException
from book.services import BookService
from review.services import ReviewService


class ReviewCreateFieldValidator(FieldValidator):
    book_id = serializers.IntegerField(min_value=1)
    rating = serializers.IntegerField(min_value=1, max_value=5)


class ReviewUpdateFieldValidator(FieldValidator):
    book_id = serializers.IntegerField(min_value=1)
    rating = serializers.IntegerField(min_value=1, max_value=5)


class ReviewDeleteFieldValidator(FieldValidator):
    book_id = serializers.IntegerField(min_value=1)


class BookExistsValidator(BaseValidator):

    def validate_request_data(self, **kwargs):
        book_id = kwargs.get("book_id")
        book = BookService.read_one(id=("=", book_id))
        if not book:
            raise APIException("BOOK_NOT_FOUND")


class BookNotAlreadyRatedByUserValidator(BaseValidator):

    def validate_request(self, request):
        user_id = request.user.id
        book_id = request.data.get("book_id")
        review = ReviewService.read_one(
            user_id=(
                "=",
                user_id,
            ),
            book_id=("=", book_id),
        )
        if review:
            raise APIException("BOOK_ALREADY_RATED_BY_USER")


class BookBeenRatedByUserValidator(BaseValidator):

    def validate_request(self, request):
        user_id = request.user.id
        book_id = request.data.get("book_id")
        review = ReviewService.read_one(
            user_id=("=", user_id),
            book_id=("=", book_id),
        )

        if not review:
            raise APIException("BOOK_NOT_BEEN_RATED_BY_USER")
