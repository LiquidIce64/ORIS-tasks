from functools import wraps
from flask import redirect, url_for, session


def check_permission(*permissions: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            user_perms = session.get('permissions')
            if user_perms is None: return redirect(url_for('auth'))

            for perm in user_perms:
                if perm in permissions: return func(*args, **kwargs)

            return redirect(url_for('auth'))

        return wrapper
    return decorator
