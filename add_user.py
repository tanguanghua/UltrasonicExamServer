from app import create_app, db
from app.models import User
import hashlib


app = create_app('dev')

user_name = 'guanghua'
password = 'guanghua'
password =hashlib.md5(password.encode(encoding='utf-8')).hexdigest()

with app.app_context() as app_ctx:
    guanghua = User(user_name=user_name, password=password, mobile='18684798169', email='guanghuatan@gmail.com')
    db.session.add(guanghua)
    try:
        db.session.commit()
    except Exception as ex:
        db.session.rollback()
        print(ex)
