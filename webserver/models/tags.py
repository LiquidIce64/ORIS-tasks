from typing import Iterable
from sqlite3 import Connection
from .db import connect_db


class Tags:
    @staticmethod
    @connect_db
    def get_tags(conn: Connection):
        return conn.execute('select * from tags').fetchall()

    @staticmethod
    @connect_db
    def get_tag(conn: Connection, tag_id: int):
        return conn.execute('select * from tags where id = ?', (tag_id,)).fetchone()

    @staticmethod
    @connect_db
    def create_tag(conn: Connection, tag_name: str, color: str):
        conn.execute('insert into tags(tag_name, color) values (?, ?)', (tag_name, color))

    @staticmethod
    @connect_db
    def edit_tag(conn: Connection, tag_id: int, tag_name: str, color: str):
        conn.execute('update tags set tag_name = ?, color = ? where id = ?', (tag_name, color, tag_id))

    @staticmethod
    @connect_db
    def delete_tag(conn: Connection, tag_id: int):
        conn.execute('delete from tags where id = ?', (tag_id,))

    @staticmethod
    @connect_db
    def set_thread_tags(conn: Connection, thread_id: int, tag_ids: Iterable[int]):
        conn.execute('delete from thread_tags where thread_id = ?', (thread_id,))
        for tag_id in tag_ids:
            conn.execute('insert into thread_tags(thread_id, tag_id) values (?, ?)', (thread_id, tag_id))

    @staticmethod
    @connect_db
    def get_thread_tags(conn: Connection, thread_id: int):
        return conn.execute('''
            select id, tag_name, color
            from thread_tags
            join tags on id = tag_id
            where thread_id = ?
        ''', (thread_id,)).fetchall()
