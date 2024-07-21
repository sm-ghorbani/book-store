from api_tools.db.services import BaseService


class SuggestionService(BaseService):

    @classmethod
    def get_user_book_suggestions(cls, user_id: int):
        sql = """
            WITH user_genre_ratings AS (
            SELECT
                b.genre,
                AVG(r.rating) AS average_rating
            FROM
                reviews r
            JOIN
                books b ON r.book_id = b.id
            WHERE
                r.user_id = %s
            GROUP BY
                b.genre
            ),
            books_not_reviewed AS (
                SELECT
                    b.id,
                    b.title,
                    b.author,
                    b.genre
                FROM
                    books b
                LEFT JOIN
                    reviews r ON b.id = r.book_id
                    AND r.user_id = %s
                WHERE
                    r.id IS NULL
            ),
            ranked_books AS (
                SELECT
                    bnr.id,
                    bnr.title,
                    bnr.author,
                    bnr.genre,
                    ugr.average_rating
                FROM
                    books_not_reviewed bnr
                JOIN
                    user_genre_ratings ugr ON bnr.genre = ugr.genre
            )
            SELECT
                rb.id,
                rb.title,
                rb.author,
                rb.genre
            FROM
                ranked_books rb
            ORDER BY
                rb.average_rating DESC
            LIMIT 10;
            """
        return cls.execute_query(sql, (user_id, user_id))
