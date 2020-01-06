from app import create_app, db
# from flask_script import Manager, Shell
from flask import current_app

app = create_app('dev')


@app.route('/')
@app.route('/index')
def index():
    return 'Hello world'


# app_ctx = app.app_context()
# app_ctx.push()

with app.app_context() as app_ctx:
    print('app name: ' + current_app.name)

    from app.models import *

    # db.drop_all()
    db.create_all()
# app_ctx.pop()

# Add interactive project shell
# def make_shell_context():
#     return dict(app=app, db=db)
# manager = Manager(app)
# manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    # manager.run()
    app.run()
