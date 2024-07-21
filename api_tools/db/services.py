from django.db import connection
from collections import namedtuple


class BaseService:
    table_name = None

    @classmethod
    def _read(cls, **kwargs):
        cursor = connection.cursor()
        sql = f"SELECT * FROM {cls.table_name}"

        if kwargs:
            conditions = [f"{key} = %s" for key in kwargs]
            sql += " WHERE " + " AND ".join(conditions)
            parameters = list(kwargs.values())
        else:
            parameters = []

        cursor.execute(sql, parameters)
        return cursor

    @classmethod
    def _get_column_names(cls, cursor):
        return [desc[0] for desc in cursor.description]

    @classmethod
    def _row_to_object(cls, row, column_names):
        RowObject = namedtuple("RowObject", column_names)
        return RowObject._make(row)

    @classmethod
    def read_all(cls, **kwargs):
        cursor = cls._read(**kwargs)
        column_names = cls._get_column_names(cursor)
        rows = cursor.fetchall()
        cursor.close()
        return [cls._row_to_object(row, column_names) for row in rows]

    @classmethod
    def read_one(cls, **kwargs):
        cursor = cls._read(**kwargs)
        column_names = cls._get_column_names(cursor)
        row = cursor.fetchone()
        cursor.close()
        if row:
            return cls._row_to_object(row, column_names)
        return None
