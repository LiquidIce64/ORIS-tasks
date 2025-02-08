from typing import Iterable
from sqlite3 import Connection
from .db import connect_db


class Permissions:
    @staticmethod
    @connect_db
    def get_permissions(conn: Connection):
        return conn.execute('select * from permissions').fetchall()

    @staticmethod
    @connect_db
    def create_permission(conn: Connection, permission_name: str):
        conn.execute('insert into permissions(permission_name) values (?)', (permission_name,))

    @staticmethod
    @connect_db
    def give_permission(conn: Connection, user_id: int, permission_id: int):
        conn.execute('insert into user_permissions(user_id, permission_id) values (?, ?)', (user_id, permission_id))

    @staticmethod
    @connect_db
    def revoke_permission(conn: Connection, user_id: int, permission_id: int):
        conn.execute('delete from user_permissions where user_id = ? and permission_id = ?', (user_id, permission_id))

    @staticmethod
    @connect_db
    def set_permissions(conn: Connection, user_id: int, permission_ids: Iterable[int]):
        conn.execute('delete from user_permissions where user_id = ?', (user_id,))
        conn.commit()
        for permission_id in permission_ids:
            Permissions.give_permission(user_id, permission_id)

    @staticmethod
    @connect_db
    def get_user_permissions(conn: Connection, user_id: int):
        return conn.execute('''
            select id, permission_name
            from user_permissions
            join permissions on id = permission_id
            where user_id = ?
        ''', (user_id,)).fetchall()

    @staticmethod
    @connect_db
    def user_has_permission(conn: Connection, user_id: int, permission_name: str):
        return conn.execute('''
            select
                id in (
                    select permission_id
                    from user_permissions
                    where user_id = ?
                ) as result
            from permissions
            where permission_name = ?
        ''', (user_id, permission_name)).fetchone()['result']
