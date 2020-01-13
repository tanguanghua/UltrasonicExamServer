from flask import request, Blueprint, session
from app.models.login import post_login
from app.utils.warp import success, fail

login_page = Blueprint('login', __name__, url_prefix='/login')


@login_page.route('', methods=['POST'])
def login():
    data = request.json
    username = data.get('user_name')
    password = data.get('password')

    if username is None or password is None or \
            username == '' or password == '':
        return fail('login information is in bad format')

    user = post_login(username, password)

    session['type'] = user.user_type

    ret = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'mobile': user.mobile
    }

    return success(ret)
