from django.db import connection


class RawObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class BaseService:
    table_name = None

    @classmethod
    def get_cursor(cls, query, params=None):
        cursor = connection.cursor()
        cursor.execute(query, params)
        return cursor

    @classmethod
    def execute_query(cls, query, params=None):
        cursor = cls.get_cursor(query, params)
        column_names = cls._get_column_names(cursor)
        rows = cursor.fetchall()
        cursor.close()
        return [cls._row_to_object(row, column_names) for row in rows]

    @classmethod
    def read_all(cls, **kwargs):
        sql, parameter = cls._read(**kwargs)
        return cls.execute_query(sql, parameter)

    @classmethod
    def read_one(cls, **kwargs):
        sql, parameter = cls._read(**kwargs)
        cursor = cls.get_cursor(sql, parameter)
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

    @classmethod
    def _read(cls, **kwargs):
        sql = f"SELECT * FROM {cls.table_name}"

        if kwargs:
            conditions = []
            parameters = []
            for key, (operator, value) in kwargs.items():
                conditions.append(f"{key} {operator} %s")
                parameters.append(value)
            sql += " WHERE " + " AND ".join(conditions)
        else:
            parameters = []

        return sql, parameters

    @classmethod
    def create(cls, **kwargs):
        columns = ", ".join(kwargs.keys())
        values = ", ".join(["%s"] * len(kwargs))
        sql = f"INSERT INTO {cls.table_name} ({columns}) VALUES ({values})"
        cursor = cls.get_cursor(sql, list(kwargs.values()))
        cursor.close()

    @classmethod
    def update(cls, set_values, **conditions):
        sql = f"UPDATE {cls.table_name} SET "

        set_clauses = []
        set_parameters = []
        for column, value in set_values.items():
            set_clauses.append(f"{column} = %s")
            set_parameters.append(value)

        sql += ", ".join(set_clauses)

        if conditions:
            condition_clauses = []
            condition_parameters = []
            for key, (operator, value) in conditions.items():
                condition_clauses.append(f"{key} {operator} %s")
                condition_parameters.append(value)
            sql += " WHERE " + " AND ".join(condition_clauses)
            parameters = set_parameters + condition_parameters
        else:
            parameters = set_parameters
        try:
            cursor = cls.get_cursor(sql, parameters)
            cursor.close()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def delete(cls, **conditions):
        sql = f"DELETE FROM {cls.table_name}"

        if conditions:
            condition_clauses = []
            parameters = []
            for key, (operator, value) in conditions.items():
                condition_clauses.append(f"{key} {operator} %s")
                parameters.append(value)
            sql += " WHERE " + " AND ".join(condition_clauses)
        else:
            parameters = []

        try:
            cursor = cls.get_cursor(sql, parameters)
            cursor.close()
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def _get_column_names(cls, cursor):
        return [desc[0] for desc in cursor.description]

    @classmethod
    def _row_to_object(cls, row, column_names):
        return RawObject(**dict(zip(column_names, row)))
