from functools import wraps
from flask import session
from app.utils.warp import fail


class Permission:
    """
    用户角色枚举类
    """
    ROOT = 0x1
    ADMIN = 0x2
    USER = 0x4

    ROLE_MAP = {
        1: 0x1,
        2: 0x2,
        3: 0x4
    }


def auth_require(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_role = session['type']
            if Permission.ROLE_MAP[int(user_role)] & role != Permission.ROLE_MAP[int(user_role)]:
                return fail('You don\'t have auth')
            return func(*args, **kwargs)

        return wrapper

    return decorator
