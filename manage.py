from app import create_app

app = create_app()

with app.app_context() as app_ctx:
    from app.models.models import *

    # db.drop_all()
    db.create_all()

# Add interactive project shell
# def make_shell_context():
#     return dict(app=app, db=db)
# manager = Manager(app)
# manager.add_command('shell', Shell(make_context=make_shell_context))


if __name__ == '__main__':
    app.run()
