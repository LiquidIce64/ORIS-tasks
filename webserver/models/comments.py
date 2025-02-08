from sqlite3 import Connection
from .db import connect_db


class Comments:
    @staticmethod
    @connect_db
    def get_comments(conn: Connection, thread_id: int):
        return conn.execute('''
            select
                comments.id, thread_id, comment_text,
                user_id, username, display_name, date_posted
            from comments
            left join users on users.id = user_id
            where thread_id = ?
        ''', (thread_id,)).fetchall()

    @staticmethod
    @connect_db
    def get_comment(conn: Connection, comment_id: int):
        return conn.execute('''
            select
                comments.id, thread_id, comment_text,
                user_id, username, display_name, date_posted
            from comments
            left join users on users.id = user_id
            where comments.id = ?
        ''', (comment_id,)).fetchone()

    @staticmethod
    @connect_db
    def create_comment(conn: Connection, thread_id: int, user_id: int, comment_text: str):
        conn.execute(
            'insert into comments(thread_id, user_id, comment_text) values (?, ?, ?)',
            (thread_id, user_id, comment_text)
        )

    @staticmethod
    @connect_db
    def edit_comment(conn: Connection, comment_id: int, comment_text: str):
        conn.execute('update comments set comment_text = ? where id = ?', (comment_text, comment_id))

    @staticmethod
    @connect_db
    def delete_comment(conn: Connection, comment_id: int):
        conn.execute('delete from comments where id = ?', (comment_id,))
