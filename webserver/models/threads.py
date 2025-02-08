from typing import Iterable
from sqlite3 import Connection
from .db import connect_db
from .tags import Tags


class Threads:
    @staticmethod
    @connect_db
    def get_threads(conn: Connection):
        return conn.execute('''
            select
                threads.id, title, description,
                author_id, username, display_name, date_posted
            from threads
            left join users on users.id = author_id
        ''').fetchall()

    @staticmethod
    @connect_db
    def get_thread(conn: Connection, thread_id: int):
        return conn.execute('''
            select
                threads.id, title, description,
                author_id, username, display_name, date_posted
            from threads
            left join users on users.id = author_id
            where threads.id = ?
        ''', (thread_id,)).fetchone()

    @staticmethod
    @connect_db
    def create_thread(conn: Connection, user_id: int, title: str, description: str, tag_ids: Iterable[int]):
        row_id = conn.execute(
            'insert into threads(author_id, title, description) values (?, ?, ?)',
            (user_id, title, description)
        ).lastrowid
        thread_id = conn.execute('select id from threads where rowid = ?', (row_id,)).fetchone()['id']
        conn.commit()
        Tags.set_thread_tags(thread_id, tag_ids)
        return thread_id

    @staticmethod
    @connect_db
    def edit_thread(conn: Connection, thread_id: int, title: str, description: str, tag_ids: Iterable[int]):
        conn.execute('update threads set title = ?, description = ? where id = ?', (title, description, thread_id))
        conn.commit()
        Tags.set_thread_tags(thread_id, tag_ids)

    @staticmethod
    @connect_db
    def delete_thread(conn: Connection, thread_id: int):
        conn.execute('delete from threads where id = ?', (thread_id,))
