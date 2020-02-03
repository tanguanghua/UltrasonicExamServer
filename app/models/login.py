from app.models.models import User


def post_login(username: str, password: str) -> User:
    user = User.query.filter_by(username=username).first()
    if not user:
        raise RuntimeError(f'{username} does not exist')

    if user.password != password:
        raise RuntimeError('password is incorrect')

    return user
