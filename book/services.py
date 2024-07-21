from api_tools.db.services import BaseService


class BookService(BaseService):
    table_name = "books"

    @classmethod
    def get_books_with_user_reviews(cls, user_id):
        query = f"""
            SELECT {cls.table_name}.*, reviews.rating AS rate
            FROM {cls.table_name}
            LEFT JOIN reviews ON {cls.table_name}.id = reviews.book_id
            AND reviews.user_id = %s
        """
        return cls.execute_query(query, (user_id,))

    @classmethod
    def get_books_with_genre(cls, user_id, genre):
        query = f"""
            SELECT {cls.table_name}.*, reviews.rating AS rate
            FROM {cls.table_name}
            LEFT JOIN reviews ON {cls.table_name}.id = reviews.book_id
            AND reviews.user_id = %s
            WHERE {cls.table_name}.genre ILIKE %s
        """
        return cls.execute_query(
            query,
            (
                user_id,
                genre,
            ),
        )
