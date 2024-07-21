from django.db import connection


class RawObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


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
        return RawObject(**dict(zip(column_names, row)))

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

    @classmethod
    def like(cls, column, value):
        cursor = connection.cursor()
        sql = f"SELECT * FROM {cls.table_name} WHERE {column} ILIKE %s"
        cursor.execute(sql, [value])
        rows = cursor.fetchall()
        if rows:
            column_names = [desc[0] for desc in cursor.description]
            cursor.close()
            return [cls._row_to_object(row, column_names) for row in rows]
        return []
