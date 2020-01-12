from flask import request, Blueprint
from app.models.login import post_login
from app.utils.warp import success, fail

login = Blueprint('api', __name__, url_prefix='/login')


@login.route('', methods=['POST'])
def login():
    data = request.json
    username = data.get('user_name')
    password = data.get('password')

    if username is None or password is None or \
            username == '' or password == '':
        return fail('login information is in bad format')

    user = post_login(username, password)

    ret = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'mobile': user.mobile
    }

    return success(ret)
