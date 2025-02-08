import os
import sqlite3 as sql
from .tags import Tags
from .users import Users
from .threads import Threads
from .comments import Comments
from .permissions import Permissions

if not os.path.exists('database.db'):
    print('Database not found, creating a new one...')
    conn = sql.connect('database.db')
    conn.row_factory = sql.Row

    conn.executescript(open('models/init_database.sql', 'r').read())
    conn.commit()

    Permissions.create_permission('Administration')
    Permissions.create_permission('Thread moderation')
    Permissions.create_permission('Tag editing')

    Users.add_user('admin', 'admin')
    Permissions.set_permissions(Users.get_user_id('admin'), (1, 2, 3))
