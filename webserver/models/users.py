from __future__ import annotations

from sqlite3 import Connection
from .db import connect_db
from .permissions import Permissions


class Users:
    @staticmethod
    @connect_db
    def get_users(conn: Connection):
        return conn.execute('select * from users').fetchall()

    @staticmethod
    @connect_db
    def get_user(conn: Connection, user_id: int):
        return conn.execute('select * from users where id = ?', (user_id,)).fetchone()

    @staticmethod
    @connect_db
    def add_user(conn: Connection, username: str, password: str):
        conn.execute('insert into users(username, display_name, password) values (?, ?, ?)', (username, username, password))

    @staticmethod
    @connect_db
    def delete_user(conn: Connection, user_id: int):
        conn.execute('delete from users where id = ?', (user_id,))

    @staticmethod
    @connect_db
    def get_user_id(conn: Connection, username: str):
        return conn.execute('select id from users where username = ?', (username,)).fetchone()['id']

    @staticmethod
    @connect_db
    def set_username(conn: Connection, user_id: int, username: str):
        conn.execute('update users set username = ? where id = ?', (username, user_id))

    @staticmethod
    @connect_db
    def get_display_name(conn: Connection, user_id: int):
        return conn.execute('select display_name from users where id = ?', (user_id,)).fetchone()['display_name']

    @staticmethod
    @connect_db
    def set_display_name(conn: Connection, user_id: int, display_name: str):
        conn.execute('update users set display_name = ? where id = ?', (display_name, user_id))

    @staticmethod
    @connect_db
    def get_password(conn: Connection, username: str) -> str | None:
        res = conn.execute('select password from users where username = ?', (username,)).fetchone()
        return None if res is None else res['password']

    @staticmethod
    @connect_db
    def set_password(conn: Connection, user_id: int, password: str):
        conn.execute('update users set password = ? where id = ?', (password, user_id))

    @staticmethod
    @connect_db
    def get_email(conn: Connection, user_id: int):
        return conn.execute('select email from users where id = ?', (user_id,)).fetchone()['email']

    @staticmethod
    @connect_db
    def set_email(conn: Connection, user_id: int, email: str):
        conn.execute('update users set email = ? where id = ?', (email, user_id))

    @staticmethod
    @connect_db
    def get_phone_number(conn: Connection, user_id: int):
        return conn.execute('select phone_number from users where id = ?', (user_id,)).fetchone()['phone_number']

    @staticmethod
    @connect_db
    def set_phone_number(conn: Connection, user_id: int, phone_number: str):
        conn.execute('update users set phone_number = ? where id = ?', (phone_number, user_id))
