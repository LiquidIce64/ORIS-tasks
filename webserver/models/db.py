from functools import wraps
import sqlite3 as sql


def connect_db(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        conn = sql.connect('database.db')
        conn.row_factory = sql.Row
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper
